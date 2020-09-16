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
if __name__ == "main":
    app.run(debug=True)
