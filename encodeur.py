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

from keras.datasets import mnist

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

print("X_train", X_train.shape)
print("X_test", X_test.shape)

def show_face_data(nparray, n=10, title=""):
    plt.figure(figsize=(30, 5))
    for i in range(n):
        ax = plt.subplot(2,n,i+1)
        plt.imshow(array_to_img(nparray[i]))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.suptitle(title, fontsize = 20)

show_face_data(X_train, title="X train")
show_face_data(X_test, title="X test")

input_layer = Input(shape=(218, 178, 3), name="INPUT")
x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_layer)
x = MaxPooling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)

code_layer = MaxPooling2D((2, 2), name="CODE")(x)

x = Conv2DTranspose(8, (3, 3), activation='relu', padding='same')(code_layer)
x = UpSampling2D((2, 2))(x)
x = Conv2DTranspose(8, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2DTranspose(16, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2,2))(x)
output_layer = Conv2D(3, (3, 3), padding='same', name="OUTPUT")(x)

AE = Model(input_layer, output_layer)
AE.compile(optimizer='adam', loss='mse')
AE.summary()