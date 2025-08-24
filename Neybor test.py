#How to Preprocess Images for Text OCR in Python 

import os
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

# ouvrir une image
image_file = "temp/compteur.jpg"

# vérifier que l'image existe et la charger
if not os.path.exists(image_file):
    raise FileNotFoundError(f"Image file not found: {image_file}")

img = cv.imread(image_file)
if img is None:
    raise ValueError(f"Failed to load image: {image_file}")

# Fonction d'affichage avec correction des couleurs BGR -> RGB
def display_cv_image(image, title="Image"):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # conversion pour affichage correct
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis('off')  # cacher les axes
    plt.show(block=True)  # important: bloque l'exécution jusqu'à fermeture

# afficher l'image originale
display_cv_image(img, "Original")

# inverser les couleurs de l'image et enregistrer
inverted_image = cv.bitwise_not(img)
output_file = "temp/inverted.jpg"
cv.imwrite(output_file, inverted_image)

# afficher l'image inversée
display_cv_image(inverted_image, "Inversée")

# Rescaling
# Binarization
def grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

gray_image = grayscale(img)
gray_file = "temp/gray.jpg"
cv.imwrite(gray_file, gray_image)

# afficher l'image en niveaux de gris
plt.imshow(gray_image, cmap='gray')
plt.title("Gris")
plt.axis('off')
plt.show()

# seuillage binaire
_, im_bw = cv.threshold(gray_image, 100, 255, cv.THRESH_BINARY)
cv.imwrite("temp/bw_image.jpg", im_bw)

# afficher l'image en noir et blanc
plt.imshow(im_bw, cmap='gray')
plt.title("Noir et Blanc")
plt.axis('off')
plt.show()

# Noise removal
def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv.dilate(image, kernel, iterations=1)
    image = cv.erode(image, kernel, iterations=1)
    image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
    image = cv.medianBlur(image, 3)
    return(image)

no_noise = noise_removal(im_bw)
cv.imwrite("temp/no_noise.jpg", no_noise)
display_cv_image(no_noise, "No Noise")

# Dilation and Erosion
def thin_font(image):
    image = cv.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv.erode(image, kernel, iterations=1)
    image = cv.bitwise_not(image)
    return(image)

eroded_image = thin_font(no_noise)
cv.imwrite("temp/eroded_image.jpg", eroded_image)
display_cv_image(eroded_image, "Eroded")

#Thick font
def thick_font(image):
    image = cv.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv.dilate(image, kernel, iterations=1)
    image = cv.bitwise_not(image)
    return(image)

dilated_image = thick_font(no_noise)
cv.imwrite("temp/dilated_image.jpg", dilated_image)
display_cv_image(dilated_image, "dilated")

#Rotation / Deskewing
new = cv.imread("temp/dilated_image.jpg")

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv.cvtColor(newImage, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 0)
    thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (30, 5))
    dilate = cv.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv.findContours(dilate, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv.contourArea, reverse = True)
    for c in contours:
        rect = cv.boundingRect(c)
        x,y,w,h = rect
        cv.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv.minAreaRect(largestContour)
    cv.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv.warpAffine(newImage, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

fixed = deskew(new)
cv.imwrite("temp/fixed.jpg", fixed)
display_cv_image(fixed, "Deskewed")

#Removing borders
def remove_borders(image):
    contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return(crop)

no_borders = remove_borders(no_noise)
cv.imwrite("temp/no_borders.jpg", no_borders)
display_cv_image(no_borders, "No Borders")

# Missing borders
color = [255, 255, 255]
top, bottom, left, right = [150]*4
image_with_borders = cv.copyMakeBorder(no_borders, top, bottom, left, right, cv.BORDER_CONSTANT, value = color)
cv.imwrite("temp/image_with_borders.jpg", image_with_borders)
display_cv_image(image_with_borders, "Image with Borders")

