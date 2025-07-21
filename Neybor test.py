import os
import cv2 as cv
from matplotlib import pyplot as plt

# ouvrir une image
image_file = "temp/compteur.jpg"

# vérifier que l'image existe et la charger
if not os.path.exists(image_file):
    raise FileNotFoundError(f"Image file not found: {image_file}")

img = cv.imread(image_file)
if img is None:
    raise ValueError(f"Failed to load image: {image_file}")

def display(im_path, title="Image"):
    print(f"Affichage : {im_path}")  # debug
    im_data = plt.imread(im_path)
    plt.imshow(im_data)
    plt.title(title)
    plt.axis('off')  # cacher les axes
    plt.show(block=True)  # important: bloque l'exécution jusqu'à fermeture

# afficher l'image originale
display(image_file, "Original")

# inverser les couleurs de l'image et enregistrer
inverted_image = cv.bitwise_not(img)
output_file = "temp/inverted.jpg"
cv.imwrite(output_file, inverted_image)

# afficher l'image inversée
display(output_file, "Inversée")

# Rescaling
# Binarization
def grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

gray_image = grayscale(img)
gray_file = "temp/gray.jpg"
cv.imwrite(gray_file, gray_image)

# afficher l'image en niveaux de gris
display(gray_file, "Gris")
