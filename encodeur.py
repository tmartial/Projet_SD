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
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Conv2DTranspose

#1. Importation des images et transformation en numpy array
path1 = "C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/celebA_test/celebA_test"
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

listing_parts=decoupe_liste(listing,500) #500 images

from skimage.transform import resize
for file in listing_parts[0]:
        chemin = "C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/celebA_test/celebA_test/"+file
        im = image.imread(chemin)
        resized_img = resize(im,(128,128))
        listarray.append(resized_img)
nparray = np.array(listarray)

#Création de ensemble d'entrainement et de test
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split (nparray, test_size=0.2, random_state=0)

#Mise en place du modèle pour l'encodeur
input_layer = Input(shape=(128, 128, 3), name="INPUT")
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



#Entrainement du modèle encodeur
AE.fit(X_train, X_train,
                epochs=2,
                batch_size=32,
                shuffle=True,
                validation_data=(X_test, X_test))

#Sauvegarde du modèle
AE.save("C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/encodeur.h5")

#Fonction pour obtenir le vecteur associé à l'image encodé
def auto_encoder():
    get_encoded_X = Model(inputs=AE.input, outputs=AE.get_layer("CODE").output)

    encoded = get_encoded_X.predict(X_test)
    encoded = encoded.reshape((len(X_test), 16*16*8))
    reconstructed = AE.predict(X_test)
    return encoded, reconstructed

encoded, reconstructed=auto_encoder()

#Sauvegarde du vecteur encodé
np.save("C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/vecteur_encodé.npy", encoded)

#Visualisation sur un ensemble d'image
def show_face_data(nparray, n=10, title=""):
    plt.figure(figsize=(30, 5))
    for i in range(n):
        ax = plt.subplot(2,n,i+1)
        plt.imshow(array_to_img(nparray[i]))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.suptitle(title, fontsize = 20)
    plt.show()

show_face_data(X_test, title="original faces")
show_face_data(reconstructed, title="reconstructed faces")

#Mise en place de façon analogique du modèle pour le décodeur
input_layer_decodeur = Input(shape=(16,16,8), name="INPUT")
x_decodeur = Conv2DTranspose(8, (3, 3), activation='relu', padding='same')(input_layer_decodeur)
x_decodeur = UpSampling2D((2, 2))(input_layer_decodeur)
x_decodeur = Conv2DTranspose(8, (3, 3), activation='relu', padding='same')(input_layer_decodeur)
x_decodeur = UpSampling2D((2, 2))(input_layer_decodeur)
x_decodeur = Conv2DTranspose(16, (3, 3), activation='relu', padding='same')(input_layer_decodeur)
x_decodeur = UpSampling2D((2,2))(input_layer_decodeur)
output_layer_decodeur = Conv2D(3, (3, 3), padding='same', name="OUTPUT")(input_layer_decodeur)

D = Model(input_layer_decodeur,output_layer_decodeur)
D.compile(optimizer='adam', loss='mse')

#Sauvegarde du modèle décodeur
AE.save("C:/Users/toto9/OneDrive/Documents/4BIM S2/PROJET/decodeur.h5")