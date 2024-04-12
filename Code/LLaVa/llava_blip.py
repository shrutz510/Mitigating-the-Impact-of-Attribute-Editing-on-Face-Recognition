# -*- coding: utf-8 -*-
"""Llava-Blip.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GUNyE9ppgVyOk3iUQ2BxWc2D19lB1coh

# Running Llava: a large multi-modal model on Google Colab

Run Llava model on a Google Colab!

Llava is a multi-modal image-text to text model that can be seen as an "open source version of GPT4". It yields to very nice results as we will see in this Google Colab demo.

![image/png](https://cdn-uploads.huggingface.co/production/uploads/62441d1d9fdefb55a0b7d12c/FPshq08TKYD0e-qwPLDVO.png)

The architecutre is a pure decoder-based text model that takes concatenated vision hidden states with text hidden states.

We will leverage QLoRA quantization method and use `pipeline` to run our model.
"""

!pip install -q -U transformers==4.37.2
!pip install -q bitsandbytes==0.41.3 accelerate==0.25.0

"""## Load an image

Let's use the image that has been used for Llava demo

And ask the model to describe that image!
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive')
# %cd '/content/drive/My Drive'
import requests
from PIL import Image

"""## Preparing the quantization config to load the model in 4bit precision

In order to load the model in 4-bit precision, we need to pass a `quantization_config` to our model. Let's do that in the cells below
"""

import torch
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

"""## Load the model using `pipeline`

We will leverage the `image-to-text` pipeline from transformers !
"""

from transformers import pipeline

model_id = "llava-hf/llava-1.5-7b-hf"

pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})

"""It is important to prompt the model wth a specific format, which is:
```bash
USER: <image>\n<prompt>\nASSISTANT:
```
"""

from pathlib import Path
import re

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_smiling.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person smiling?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_smiling = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_smiling, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_young.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person young?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_young = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_young, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_old.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person old?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_old = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_old, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_male.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person male?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_male = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_male, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_female.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person female?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_female = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_female, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_bald.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person bald?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_bald = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_bald, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_black hair.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have black hair?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_black_hair = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_black_hair, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_brown hair.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have brown hair?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_brown_hair = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_brown_hair, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_blond hair.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have blond hair?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_blond_hair = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_blond_hair, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_bangs.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have bangs?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_bangs = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_bangs, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_no beard.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have no beard?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_no_beard = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_no_beard, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_mustache.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a mustache?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_mustache = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_mustache, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_bushy eyebrows.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have bushy eyebrows?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_bushy_eyebrows = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_bushy_eyebrows, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_slightly open mouth.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a slightly open mouth?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_open_mouth = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_open_mouth, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_double chin.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a double chin?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_double_chin = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_double_chin, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_big nose.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a big nose?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_big_nose = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_big_nose, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_big lips.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have big lips?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_big_lips = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_big_lips, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_eyeglasses.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person wearing eyeglasses?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_eyeglasses = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_eyeglasses, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_necktie.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person wearing a necktie?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_necktie = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_necktie, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_hat.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person wearing a hat?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_hat = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_hat, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_angry.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Is the person angry?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_angry = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_angry, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_neutral expression.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a neutral expression?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_neutral_expression = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_neutral_expression, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_surprise expression.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a surprised expression?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_surprise_expression = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_surprise_expression, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_sad expression.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a sad expression?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_sad_expression = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_sad_expression, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_disgust expression.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a disgusted expression?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_disgusted_expression = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_disgusted_expression, 2)}%")

images_path = Path("/content/drive/MyDrive/Result_Blip")

images = [p for p in images_path.glob("**/*_fear expression.png")]

correct_answers = 0
total_images = 0

for img_path in images:
    image = Image.open(img_path)
    question = 'Does the person have a fearful expression?'
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # print(f"File Name: {img_path.name}")
    # print(outputs[0]["generated_text"])

    text = outputs[0]["generated_text"]
    match = re.search(r"ASSISTANT:\s+(\w+)", text)
    word = match.group(1) if match else "Not found"

    # print(f"{word}\n")

    if word == 'Yes':
      correct_answers += 1

    total_images += 1

accuracy_fear_expression = (correct_answers / total_images) * 100
print(f"Accuracy: {round(accuracy_fear_expression, 2)}%")

questions = [
    'Is the person smiling?', #done
    'Is the person young?', #done
    'Is the person old?', #done
    'Is the person male?', #done
    'Is the person female?', #done
    'Is the person bald?', #done
    'Does the person have black hair?', #done
    'Does the person have brown hair?', #done
    'Does the person have blond hair?', #done
    'Does the person have bangs?', #done
    'Does the person have no beard?', #done
    'Does the person have a mustache?', #done
    'Does the person have bushy eyebrows?', #done
    'Does the person have a slightly open mouth?', #done
    'Does the person have a double chin?', #done
    'Does the person have a big nose?', #done
    'Does the person have big lips?', #done
    'Is the person wearing eyeglasses?', #done
    'Is the person wearing a necktie?', #done
    'Is the person wearing a hat?', #done
    'Is the person angry?', #done
    'Does the person have a neutral expression?', #done
    'Does the person have a surprised expression?', #done
    'Does the person have a sad expression?', #done
    'Does the person have a disgusted expression?', #done
    'Does the person have a fearful expression?' #done
]



"""The model has managed to successfully describe the image with accurate result ! We also support other variants of Llava, such as [`bakLlava`](https://huggingface.co/llava-hf/bakLlava-v1-hf) which should be all posted inside the [`llava-hf`](https://huggingface.co/llava-hf) organization on 🤗 Hub"""

