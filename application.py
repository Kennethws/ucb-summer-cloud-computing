from flask import Flask, render_template, request
import json, os, cv2
import boto3
from base64 import b64decode
import svglib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from handwritten import handwritten
from PIL import Image

application = Flask(__name__)
alphabets = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ-' "

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


@application.route('/testpic')
def testpic():
	src = cv2.imread("TEST_9992.jpg", cv2.IMREAD_GRAYSCALE)
	resize_image = cv2.resize(src, (256, 64), interpolation=cv2.INTER_LINEAR)
	result = handwritten(resize_image)
	return render_template("testpic.html", result = result)

@application.route('/rec_example', methods = ['POST', 'GET'])
def rec_example():
	src = cv2.imread("static/img/TEST_9992.jpg", cv2.IMREAD_GRAYSCALE)
	# resize_image = cv2.resize(src, (256, 64), interpolation=cv2.INTER_LINEAR)
	result = handwritten(src)
	return result




@application.route('/signature')
def signature():
	return render_template('unmini.html')

#---------------Callback function for Ajax from JQuery---------------------------
@application.route('/recognize', methods = ['POST', 'GET'])
def recognize():
	#---------get img data(svg/base64) from jquery and generate .jpg image.------
	data_uri = request.form.get('data')
	header, encoded = data_uri.split(",", 1)
	data = b64decode(encoded)
	with open("handwritten.svg", "wb") as f: 
		f.write(data)
	drawing = svg2rlg("handwritten.svg")
	renderPM.drawToFile(drawing, "handwritten.jpg", fmt="JPG")
	if os.path.exists("handwritten.svg"):
		os.remove("handwritten.svg")
	else:
		print("The file does not exist")

	src = cv2.imread("handwritten.jpg", cv2.IMREAD_GRAYSCALE)
	# src = src.resize((256, 64),Image.ANTIALIAS)
	# src = cv2.resize(src, (256, 64), interpolation=cv2.INTER_AREA)
	# cv2.imwrite("handwritten.jpg", src)
	#----------------------Load Model-----------------------------------------
	# msg = ''
	# try:
	# 	model = load_model("model.h5")
	# except IOError:
	# 	msg = 'Error: Load model failed, no such file or directory.'
	# else:
	# 	msg = 'Model loaded!'
	result = handwritten(src)
	#-------Comment below if want to see the exact picture---------
	if os.path.exists("handwritten.jpg"):
		os.remove("handwritten.jpg")
	else:
		print("The file does not exist")
	#---------------------------------------------------------------
	return result




if __name__ == '__main__':
	application.run()
