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
_, im_bw = cv.threshold(gray_image, 90, 255, cv.THRESH_BINARY)
cv.imwrite("temp/bw_image.jpg", im_bw)

# afficher l'image en noir et blanc
plt.imshow(im_bw, cmap='gray')
plt.title("Noir et Blanc")
plt.axis('off')
plt.show()

