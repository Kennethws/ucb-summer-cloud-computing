
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
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=8080, debug=True)
=======
    app.run(host='0.0.0.0', port=8080, debug=True)
>>>>>>> 3cb85bfa1588fb9cd99544cb1a58c3cc993d6066
