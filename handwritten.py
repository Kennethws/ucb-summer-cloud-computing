import cv2
from keras import backend as K
import numpy as np
from keras.models import load_model
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, Reshape, Bidirectional, LSTM, Dense, Lambda, Activation, BatchNormalization, Dropout
from keras.optimizers import Adam


alphabets = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ-' "

def handwritten(img_data):

	max_str_len = 24 # max length of input labels
	num_of_characters = len(alphabets) + 1 # +1 for ctc pseudo blank
	num_of_timestamps = 64 # max length of predicted labels

    # Rebuild the model
	input_data = Input(shape=(256, 64, 1), name='input')

	inner = Conv2D(32, (3, 3), padding='same', name='conv1', kernel_initializer='he_normal')(input_data)
	inner = BatchNormalization()(inner)
	inner = Activation('relu')(inner)
	inner = MaxPooling2D(pool_size=(2, 2), name='max1')(inner)

	inner = Conv2D(64, (3, 3), padding='same', name='conv2', kernel_initializer='he_normal')(inner)
	inner = BatchNormalization()(inner)
	inner = Activation('relu')(inner)
	inner = MaxPooling2D(pool_size=(2, 2), name='max2')(inner)
	inner = Dropout(0.3)(inner)

	inner = Conv2D(128, (3, 3), padding='same', name='conv3', kernel_initializer='he_normal')(inner)
	inner = BatchNormalization()(inner)
	inner = Activation('relu')(inner)
	inner = MaxPooling2D(pool_size=(1, 2), name='max3')(inner)
	inner = Dropout(0.3)(inner)

    # CNN to RNN
	inner = Reshape(target_shape=((64, 1024)), name='reshape')(inner)
	inner = Dense(64, activation='relu', kernel_initializer='he_normal', name='dense1')(inner)

    ## RNN
	inner = Bidirectional(LSTM(256, return_sequences=True), name = 'lstm1')(inner)
	inner = Bidirectional(LSTM(256, return_sequences=True), name = 'lstm2')(inner)

    ## OUTPUT
	inner = Dense(num_of_characters, kernel_initializer='he_normal',name='dense2')(inner)
	y_pred = Activation('softmax', name='softmax')(inner)

	model = Model(inputs=input_data, outputs=y_pred)

	model.load_weights('web_model_weights.h5')

    # Get the result
    

	# img_dir = 'handwritten.jpg'
	# image = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)

	image = preprocess(img_data)
	image = image/255.
	pred = model.predict(image.reshape(1, 256, 64, 1))
	decoded = K.get_value(K.ctc_decode(pred, input_length=np.ones(pred.shape[0])*pred.shape[1],
                                       greedy=True)[0][0])
	result = decoded[0]
	result = str(num_to_label(result))
	
	return result

def preprocess(img):
    (h, w) = img.shape

    final_img = np.ones([64, 256])*255 # blank white image

    # crop
    if w > 256:
        img = img[:, :256]

    if h > 64:
        img = img[:64, :]


    final_img[:h, :w] = img
    return cv2.rotate(final_img, cv2.ROTATE_90_CLOCKWISE)

def num_to_label(num):
    ret = ""
    global alphabets
    for ch in num:
        if ch == -1:  # CTC Blank
            break
        else:
            ret+=alphabets[ch]
    return ret