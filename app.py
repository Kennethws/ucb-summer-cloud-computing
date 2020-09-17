from flask import Flask, render_template, request
import boto3
app = Flask(__name__)
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/boto', methods = ['POST', 'GET'])
def text_detect():
	
	if request.method == 'POST':
		comprehend = boto3.client("comprehend", region_name='us-west-2')
		text = request.form.get('text')
		language = request.form.get('language')
		result = comprehend.detect_key_phrases(Text = text, LanguageCode = language)
		return render_template("boto.html", result=result )

if __name__ == '__main__':
   app.run(debug = True)
