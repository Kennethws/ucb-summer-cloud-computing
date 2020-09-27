from flask import Flask, render_template, request
import boto3
import pickle
import tensorflow as tf
from keras.models import load_model
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
		result = comprehend.detect_key_phrases(Text = text, LanguageCode = language)
		return render_template("boto.html", result=result )

@application.route('/ml_result', methods = ['GET'])
def ml_result():
    # Reload model and other parameters
    with open('training_info.pickle', 'rb') as f:
        data = pickle.load(f)
    alphabets = data[0]
    max_str_len = data[1]
    num_of_characters = data[2]
    num_of_timestamps = data[3]
    model = load_model('model.h5')

    # Get the result picture
    test = pd.read_csv('written_name_test_v2.csv')

    plt.figure(figsize=(15, 10))
    for i in range(6):
        ax = plt.subplot(2, 3, i+1)
        img_dir = 'test_v2/test/'+test.loc[i, 'FILENAME']
        image = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)
        plt.imshow(image, cmap='gray')

        image = preprocess(image)
        image = image/255.
        pred = model_final.predict(image.reshape(1, 256, 64, 1))
        decoded = K.get_value(K.ctc_decode(pred, input_length=np.ones(pred.shape[0])*pred.shape[1],
                                           greedy=True)[0][0])
        plt.title(num_to_label(decoded[0]), fontsize=12)
        plt.axis('off')

    plt.subplots_adjust(wspace=0.2, hspace=-0.8)
    plt.savefig('../ml_result/result.png')

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
   application.run()
