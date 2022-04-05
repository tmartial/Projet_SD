from keras.models import Model, load_model

#necessary or not ?
#import tensorflow as tf


#load X_test ? 
# With X_test the initial numpy array of the faces pixels at each step


#load encoder 
def load_AE() :
    """This function loads the autoencoder model 'faces_AE.h5' that is saved in the same directory
    Parameters
    ----------
    None

    Returns
    -------
    keras.engine.functional.Functional
        Trained Auto-encoder model   
    """
    AE = load_model('faces_AE.h5')
    return AE

#load decoder 
def load_decoder() :
    """This function loads the decoder model 'faces_decod.h5' that is saved in the same directory
    Parameters
    None

    Returns
    -------
    keras.engine.functional.Functional
        Trained decoder model
    """
    decoder = load_model('faces_decod.h5')
    return decoder


#Get encoded faces (GA's input)
def get_encoded_face(my_X_test) :
    """This function takes as parameters a numpy array of vectorized colored 128*128 pictures and returns their encoded version (by the model 'faces_AE.h5')
    Parameters
    ----------
    my_X_test : numpy.ndarray
        Pixel coordinates of a set of n pictures, each with dimension (128,128,3) 

    Returns
    -------
    numpy.ndarray
        A n rows and 2048 columns array
        with n = len(my_X_test), the number of pictures encoded
    
    Examples
    --------
    >>>from keras.preprocessing import image
    >>>img = image.load_img("C:/my_img.jpg, target_size = (128,128))
    >>>1_img = image.img_to_array(img) 
    >>>print(get_encoded_face(1_img).shape)
    (1, 2048)
    """

    my_AE = load_AE()
    encoded_model = Model(inputs= my_AE.input, outputs=my_AE.get_layer("CODE").output)
    encoded_face = encoded_model.predict(my_X_test)
    encoded_face_rs = encoded_face.reshape((len(my_X_test), 16*16*8))
    return encoded_face_rs


#Takes Genetic Algo's output as an input and decodes it
def decode_faces(ga_vector):
    """This function takes as parameters a numpy array of the same size that the one returned by get_encoded_faces(), after we submitted it
    to a genetic algoithm for example, and returns their decoded version (by the model 'decod_AE.h5')

    Parameters
    ----------
    ga_vector : numpy.ndarray
        A len(ga_vector) rows and 2048 columns array
        with len(ga_vector) the number of pictures we want to decode

    Returns
    -------
    numpy.ndarray
        Pixel coordinates of a set of len(ga_vector) pictures, each with dimension (128,128,3) 
        
    Examples
    --------    
    >>> from keras.preprocessing import image
    >>> img = image.load_img("C:/my_img.jpg, target_size = (128,128))
    >>> 1_img = image.img_to_array(img) 
    >>> encoded_img = get_encoded_face(1_img))
    >>> print(decode_faces(encoded_img).shape) 
    (1, 128, 128, 3) 
    """

    my_decoder = load_decoder()
    ga_vector_rs = ga_vector.reshape(len(ga_vector), 16, 16, 8)
    decoded_faces  = my_decoder.predict(ga_vector_rs)



