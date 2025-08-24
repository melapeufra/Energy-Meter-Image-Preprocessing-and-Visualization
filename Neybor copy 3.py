import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm
from PIL import Image
import subprocess
import sys

# Optional: Automatically install keras-ocr and easyocr if not already installed
def install_if_missing(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import easyocr
except ImportError:
    install_if_missing('easyocr')
    import easyocr

try:
    import keras_ocr
except ImportError:
    install_if_missing('keras-ocr')
    import keras_ocr

plt.style.use('ggplot')

# Load annotations and image file paths
annot = pd.read_parquet('../input/textocr-text-extraction-from-images-dataset/annot.parquet')
imgs = pd.read_parquet('../input/textocr-text-extraction-from-images-dataset/img.parquet')
img_fns = glob('../input/textocr-text-extraction-from-images-dataset/train_val_images/train_images/*')

# Show the first image
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(plt.imread(img_fns[0]))
ax.axis('off')
plt.show()

# Show a grid of 25 images with annotation count
fig, axs = plt.subplots(5, 5, figsize=(20, 20))
axs = axs.flatten()
for i in range(25):
    axs[i].imshow(plt.imread(img_fns[i]))
    axs[i].axis('off')
    image_id = os.path.splitext(os.path.basename(img_fns[i]))[0]
    n_annot = len(annot.query('image_id == @image_id'))
    axs[i].set_title(f'{image_id} - {n_annot}')
plt.show()

# EasyOCR
reader = easyocr.Reader(['en'], gpu=True)

dfs = []
for img in tqdm(img_fns[:25], desc="Running EasyOCR"):
    result = reader.readtext(img)
    img_id = os.path.splitext(os.path.basename(img))[0]
    img_df = pd.DataFrame(result, columns=['bbox', 'text', 'conf'])
    img_df['img_id'] = img_id
    dfs.append(img_df)
easyocr_df = pd.concat(dfs)

# Keras OCR
pipeline = keras_ocr.pipeline.Pipeline()

dfs = []
for img in tqdm(img_fns[:25], desc="Running Keras OCR"):
    results = pipeline.recognize([img])
    result = results[0]
    img_id = os.path.splitext(os.path.basename(img))[0]
    img_df = pd.DataFrame(result, columns=['text', 'bbox'])
    img_df['img_id'] = img_id
    dfs.append(img_df)
kerasocr_df = pd.concat(dfs)

# Comparison function
def plot_compare(img_fn, easyocr_df, kerasocr_df):
    img_id = os.path.splitext(os.path.basename(img_fn))[0]
    fig, axs = plt.subplots(1, 2, figsize=(15, 10))

    # EasyOCR results
    easy_results = easyocr_df.query('img_id == @img_id')[['text', 'bbox']].values.tolist()
    easy_results = [(x[0], np.array(x[1])) for x in easy_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn), easy_results, ax=axs[0])
    axs[0].set_title('easyocr results', fontsize=20)

    # Keras OCR results
    keras_results = kerasocr_df.query('img_id == @img_id')[['text', 'bbox']].values.tolist()
    keras_results = [(x[0], np.array(x[1])) for x in keras_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn), keras_results, ax=axs[1])
    axs[1].set_title('keras_ocr results', fontsize=20)
    plt.show()

# Run comparison on 25 images
for img_fn in img_fns[:25]:
    plot_compare(img_fn, easyocr_df, kerasocr_df)

# Save OCR results to Excel files
easyocr_df.to_excel('easyocr_results.xlsx', index=False)
kerasocr_df.to_excel('kerasocr_results.xlsx', index=False)

print("✅ OCR results saved to 'easyocr_results.xlsx' and 'kerasocr_results.xlsx'")
