from flask import Flask, render_template, request
import boto3
from keras import backend as K
from keras.models import Model
from tensorflow.keras.models import load_model
from keras.layers import Input, Conv2D, MaxPooling2D, Reshape, Bidirectional, LSTM, Dense, Lambda, Activation, BatchNormalization, Dropout
from keras.optimizers import Adam
import matplotlib.pyplot as plt


application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/boto', methods = ['POST', 'GET'])
def text_detect():
    if request.method == 'POST':
        comprehend = boto3.client("comprehend", region_name='us-west-2')
        text = request.form.get('text')
        language = request.form.get('language')

        # detect key phrases
        phrase = comprehend.detect_key_phrases(Text = text, LanguageCode = language)
        score_phrase = []
        for entry in phrase['KeyPhrases']:
            for key, value in entry.items():
                if key == 'Score':
                    score_phrase.append(value)

        phrases = []
        for entry in phrase['KeyPhrases']:
            for key, value in entry.items():
                if key == 'Text':
                    phrases.append(value)

        length = len(phrases)

        # detect sentiment
        sentiment = comprehend.detect_sentiment(Text = text, LanguageCode = language)
        d = {k: v for k, v in sorted(sentiment['SentimentScore'].items(), key=lambda item: item[1], reverse=True)}

        category = []
        score_sentiment = []
        for k, v in d.items():
            category.append(k)
            score_sentiment.append(v)

        return render_template("boto.html", score_phrase=score_phrase, phrases=phrases, length=length, score_sentiment=score_sentiment, category=category)


@application.route('/ml_result', methods = ['Post', 'GET'])
def ml_result():
    # Reload parameters
    alphabets = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ-' "
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

    model.load_weights('../web_model_weights.h5')

    # Get the result
    test = pd.read_csv('written_name_test_v2.csv')

    img_dir = 'test_v2/test/TEST_9992.jpg'
    image = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)

    image = preprocess(image)
    image = image/255.
    pred = model.predict(image.reshape(1, 256, 64, 1))
    decoded = K.get_value(K.ctc_decode(pred, input_length=np.ones(pred.shape[0])*pred.shape[1],
                                       greedy=True)[0][0])
    result = decoded[0]

    return render_template('ml_result.html', result=result)

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

def label_to_num(label):
    global alphabets
    label_num = []
    for ch in label:
        label_num.append(alphabets.find(ch))

    return np.array(label_num)

def num_to_label(num):
    ret = ""
    global alphabets
    for ch in num:
        if ch == -1:  # CTC Blank
            break
        else:
            ret+=alphabets[ch]
    return ret


if __name__ == '__main__':
   application.run(host='0.0.0.0', port=8080, debug=True)
