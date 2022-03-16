import numpy as np                   # advanced math library
import matplotlib.pyplot as plt      # plotting routines
from keras.models import Model       # Model type to be used
from keras.layers.core import Dense, Dropout, Activation # Types of layers to be used in our model
from keras.utils import np_utils                         # NumPy related tools
import keras
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
from multiprocessing import Pool
import os
from PIL import Image
from matplotlib import image
from skimage import io

path1 = "C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/img_align_celeba/img_align_celeba"
listing = os.listdir(path1)
listarray = []

def decoupe_liste(liste, taille_decoupe):
    listing_parts = []
    intervalle_0 = 0
    intervalle_1 = taille_decoupe
    while intervalle_0 <=(len(liste)):
        listing_parts.append(liste[intervalle_0:intervalle_1]) 
        intervalle_0 = intervalle_1
        intervalle_1 = intervalle_1 + taille_decoupe
    return listing_parts 

listing_parts=decoupe_liste(listing,20000)
print(listing_parts)

nparray = np.array(listing_parts[0])
print(nparray)

for file in nparray:
        print(file)
        chemin = "C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/img_align_celeba/img_align_celeba/"+file
        im = io.imread(chemin)
        imarray = img_to_array(im)
        listarray.append(imarray)
print(listarray)

from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split (listing_parts[0], test_size=0.2, random_state=0)


img = array_to_img(listarray[0])
plt.imshow(img)
plt.show()
print(img.size)

img2 = array_to_img(listarray[1])
plt.imshow(img2)
plt.show()
print(img2.size)


print(listarray)

