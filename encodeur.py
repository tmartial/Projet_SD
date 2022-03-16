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

listing_parts=decoupe_liste(listing,100)
print(listing_parts)

for file in listing_parts[0]:
        chemin = "C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/img_align_celeba/img_align_celeba/"+file
        im = image.imread(chemin)
        listarray.append(im)
print(listarray)

nparray = np.array(listarray)
print(nparray)
print(nparray.shape)

img = array_to_img(nparray[0])
plt.imshow(img)
plt.show()

from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split (nparray, test_size=0.2, random_state=0)

