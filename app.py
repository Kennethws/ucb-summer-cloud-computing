
import boto3
from flask import Flask, render_template
#
# comprehend = boto3.client("comprehend")
#
# text = input("Please enter a message:")
# language = input("Please enter your language:")
#
# print(comprehend.detect_key_phrases(Text = text, LanguageCode = language))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/')
def hello():
    return 'Hello!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)