import net
import torch
import os
from face_alignment import align
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import cv2
import io
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter
from sklearn import manifold
from sklearn.utils import check_random_state


# Define paths and model details
adaface_models = {
    'ir_50': "pretrained/adaface_ir50_ms1mv2.ckpt",
}

def load_pretrained_model(architecture='ir_50'):
    # Load model and pretrained state dictionary
    assert architecture in adaface_models.keys(), "Architecture not found in the predefined models."
    model = net.build_model(architecture)
    statedict = torch.load(adaface_models[architecture], map_location=torch.device('cpu'))['state_dict']
    model_statedict = {key[6:]: val for key, val in statedict.items() if key.startswith('model.')}
    model.load_state_dict(model_statedict)
    model.eval()
    return model

def to_input(pil_rgb_image):
    # Preprocess image for model input
    np_img = np.array(pil_rgb_image)
    if np_img.shape != (112, 112, 3):
        return None
    brg_img = ((np_img[:, :, ::-1] / 255.) - 0.5) / 0.5
    tensor = torch.tensor([brg_img.transpose(2, 0, 1)], dtype=torch.float)
    return tensor

if __name__ == '__main__':
    model = load_pretrained_model('ir_50')

    # Paths for images
    test_image_path = '/scratch/sgw6735/InstantID/Result_CNIP'
    
    features_test1 = []
    features_test2 = []
    features_test3 = []

    for fname in sorted(os.listdir(test_image_path)):
        if fname.endswith(f"_black hair.png"):
            path = os.path.join(test_image_path, fname)
            if not os.path.exists(path):
                continue
            aligned_rgb_img = align.get_aligned_face(path)
            bgr_tensor_input = to_input(aligned_rgb_img)
            if bgr_tensor_input is None:
                continue
            feature, _ = model(bgr_tensor_input)
            features_test1.append(feature.squeeze().detach().numpy())

    for fname in sorted(os.listdir(test_image_path)):
        if fname.endswith(f"_brown hair.png"):
            path = os.path.join(test_image_path, fname)
            if not os.path.exists(path):
                continue
            aligned_rgb_img = align.get_aligned_face(path)
            bgr_tensor_input = to_input(aligned_rgb_img)
            if bgr_tensor_input is None:
                continue
            feature, _ = model(bgr_tensor_input)
            features_test2.append(feature.squeeze().detach().numpy())

    for fname in sorted(os.listdir(test_image_path)):
        if fname.endswith(f"_blonde hair.png"):
            path = os.path.join(test_image_path, fname)
            if not os.path.exists(path):
                continue
            aligned_rgb_img = align.get_aligned_face(path)
            bgr_tensor_input = to_input(aligned_rgb_img)
            if bgr_tensor_input is None:
                continue
            feature, _ = model(bgr_tensor_input)
            features_test3.append(feature.squeeze().detach().numpy())

    M = np.stack(features_test1)
    N = np.stack(features_test2)
    P = np.stack(features_test3)
    
    # Combine all the features
    arr = np.concatenate((M, N, P), axis=0)
    
    # Keep track of the indices where each category starts
    orig_mid = M.shape[0]
    test1_mid = orig_mid + N.shape[0]

    # Initialize and fit t-SNE
    tsne = manifold.TSNE(n_components=3, init='pca', random_state=0, perplexity=30, n_iter=5000)
    trans_data = tsne.fit_transform(arr)

    # Plotting
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Rotate the view
    ax.view_init(elev=20, azim=130)  

    # Use indexing to plot the different sections of trans_data
    ax.scatter(trans_data[:orig_mid, 0], trans_data[:orig_mid, 1], trans_data[:orig_mid, 2], c='red', s=100, marker='.', label='Black Hair')
    ax.scatter(trans_data[orig_mid:test1_mid, 0], trans_data[orig_mid:test1_mid, 1], trans_data[orig_mid:test1_mid, 2], c='blue', s=100, marker='.', label='Brown Hair')
    ax.scatter(trans_data[test1_mid:, 0], trans_data[test1_mid:, 1], trans_data[test1_mid:, 2], c='green', s=100, marker='.', label='Blonde Hair')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title("3D t-SNE for Hair Color - CN-IP")
    plt.legend()
    plt.axis('tight')

    # Saving plot with matplotlib, then using cv2 to save the image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Read buffer with OpenCV
    image = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(image, 1)

    # Save image with OpenCV
    cv2.imwrite(f'./tsne/blip_hair3.png', image)