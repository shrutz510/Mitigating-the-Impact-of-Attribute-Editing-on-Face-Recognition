import cv2
import torch
import numpy as np
from PIL import Image

from diffusers.utils import load_image
from diffusers.models import ControlNetModel
from diffusers.pipelines.controlnet.multicontrolnet import MultiControlNetModel

from insightface.app import FaceAnalysis
from pipeline_stable_diffusion_xl_instantid_full import StableDiffusionXLInstantIDPipeline, draw_kps

from controlnet_aux import MidasDetector

import os

def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def resize_img(input_image, max_side=1280, min_side=1024, size=None, 
               pad_to_max_side=False, mode=Image.BILINEAR, base_pixel_number=64):

    w, h = input_image.size
    if size is not None:
        w_resize_new, h_resize_new = size
    else:
        ratio = min_side / min(h, w)
        w, h = round(ratio*w), round(ratio*h)
        ratio = max_side / max(h, w)
        input_image = input_image.resize([round(ratio*w), round(ratio*h)], mode)
        w_resize_new = (round(ratio * w) // base_pixel_number) * base_pixel_number
        h_resize_new = (round(ratio * h) // base_pixel_number) * base_pixel_number
    input_image = input_image.resize([w_resize_new, h_resize_new], mode)

    if pad_to_max_side:
        res = np.ones([max_side, max_side, 3], dtype=np.uint8) * 255
        offset_x = (max_side - w_resize_new) // 2
        offset_y = (max_side - h_resize_new) // 2
        res[offset_y:offset_y+h_resize_new, offset_x:offset_x+w_resize_new] = np.array(input_image)
        input_image = Image.fromarray(res)
    return input_image


if __name__ == "__main__":

    # Load face encoder
    app = FaceAnalysis(name='antelopev2', root='/home/sgw6735/.insightface/', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    # Path to InstantID models
    face_adapter = './checkpoints/ip-adapter.bin'
    controlnet_path = './checkpoints/ControlNetModel'
    controlnet_depth_path = 'diffusers/controlnet-depth-sdxl-1.0-small'
    
    # Load depth detector
    midas = MidasDetector.from_pretrained("lllyasviel/Annotators")

    # Load pipeline
    controlnet_list = [controlnet_path, controlnet_depth_path]
    controlnet_model_list = []
    for path in controlnet_list:
        controlnet = ControlNetModel.from_pretrained(path, torch_dtype=torch.float16)
        controlnet_model_list.append(controlnet)
    controlnet = MultiControlNetModel(controlnet_model_list)
    
    base_model_path = 'stabilityai/stable-diffusion-xl-base-1.0'

    pipe = StableDiffusionXLInstantIDPipeline.from_pretrained(
        base_model_path,
        controlnet=controlnet,
        torch_dtype=torch.float16,
    )
    pipe.cuda()
    pipe.load_ip_adapter_instantid(face_adapter)

    attributes = ["bangs", "big lips", "big nose", "black hair", "brown hair", "blond hair", "bushy eyebrows", "disgust expression", "double chin", "fear expression", "mustache", "neutral expression", "no beard", "sad expression", "slightly open mouth"]

    prompt = "(lowres, low quality, worst quality:1.2), (text:1.2), blue eyes, flat, low contrast, oversaturated, underexposed, overexposed, blurred, noisy, watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured"

    for attribute in attributes:
        n_prompt = f"HDR colored photo of person with {attribute}. High dynamic range, vivid, rich details, clear shadows and highlights, realistic, intense, enhanced contrast, highly detailed"

        for i in range(101):
            image_filename = f"./Images/{i}.jpg"

            if not os.path.exists(image_filename):
                print(f"Image not found: {image_filename}")
                continue
            
            try: 
                face_image = load_image(image_filename)
                face_image = resize_img(face_image)

                face_info = app.get(cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR))
                face_info = sorted(face_info, key=lambda x: (x['bbox'][2]-x['bbox'][0])*x['bbox'][3]-x['bbox'][1])[-1]  # only use the maximum face
                face_emb = face_info['embedding']

                # Use another reference image
                pose_image = load_image(image_filename)
                pose_image = resize_img(pose_image)

                face_info = app.get(cv2.cvtColor(np.array(pose_image), cv2.COLOR_RGB2BGR))
                pose_image_cv2 = convert_from_image_to_cv2(pose_image)
                face_info = sorted(face_info, key=lambda x: (x['bbox'][2]-x['bbox'][0])*x['bbox'][3]-x['bbox'][1])[-1]  # only use the maximum face
                face_kps = draw_kps(pose_image, face_info['kps'])

                width, height = face_kps.size

                # Use depth control
                processed_image_midas = midas(pose_image)
                processed_image_midas = processed_image_midas.resize(pose_image.size)
                
                # Enhance face region
                control_mask = np.zeros([height, width, 3])
                x1, y1, x2, y2 = face_info["bbox"]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                control_mask[y1:y2, x1:x2] = 255
                control_mask = Image.fromarray(control_mask.astype(np.uint8))

                image = pipe(
                    prompt=prompt,
                    negative_prompt=n_prompt,
                    image_embeds=face_emb,
                    control_mask=control_mask,
                    image=[face_kps, processed_image_midas],
                    controlnet_conditioning_scale=[0.8,0.8],
                    ip_adapter_scale=0.1,
                    num_inference_steps=30,
                    guidance_scale=5,
                ).images[0]

                image.save(f'./Result/result_{i}_{attribute}.jpg')

            except Exception as e:
                print(f"Error processing {image_filename}: {e}")
