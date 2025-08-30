import pytesseract
from PIL import Image
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img_file = "temp/no_noise.jpg"
#no_noise = 

img = Image.open(img_file)
ocr_result = pytesseract.image_to_string(img)

df = pd.DataFrame([{"Extracted Text": ocr_result.strip()}])
output_file = "ocr_output.xlsx"
df.to_excel(output_file, index=False)

print("OCR result saved to", output_file)

