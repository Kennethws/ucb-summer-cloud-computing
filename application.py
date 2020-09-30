from flask import Flask, render_template, request
import json, os
import cv2
import boto3
from base64 import b64decode
import svglib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
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

@application.route('/signature')
def jsignature():
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
	resize_image = cv2.resize(src, (256, 64), interpolation=cv2.INTER_LINEAR)
	cv2.imwrite("handwritten.jpg", resize_image)

	#-------Comment below if want to see the exact picture---------
	if os.path.exists("handwritten.jpg"):
		os.remove("handwritten.jpg")
	else:
		print("The file does not exist")
	#---------------------------------------------------------------
	
	return data


if __name__ == '__main__':
   application.run(debug=True)
