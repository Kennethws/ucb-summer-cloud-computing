from flask import Flask, render_template, request
import boto3
from base64 import b64decode
# import svglib
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF, renderPM
# import os

application = Flask(__name__)
# application.static_folder = '/Users/oscar/Downloads/templated-hielo/templates/'

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/boto_first', methods = ['POST', 'GET'])
def boto_first():
    return render_template('boto_first.html')

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

@application.route('/written_first', methods=['POST', 'GET'])
def written_first():
    return render_template("nice_unmini.html")

@application.route('/written_detect', methods=['POST', 'GET'])
def handwritten_detect():
    if request.method == 'POST':
        data_uri = request.form.get('data')
        encoded = data_uri.split(",", 1)
        data = b64decode(encoded[1])
        with open("handwritten.png", "wb") as f:
            f.write(data)

        file_name = "handwritten.png"
        # bucket = 'ucb-rekognition'
        bucket = 'handwritten-image'
        key_name = "handwritten.png"
        # create a resource of S3 to use 'Bucket' attribute
        s3_resource = boto3.client('s3')

        # upload the file as on object using put_object
        # s3_resource.Bucket(bucket).put_object(Key=file.filename, Body=file)
        s3_resource.upload_file(file_name, bucket, key_name)

        ## detect text from the image uploaded onto S3 by AWS Rekognition
        rekognition = boto3.client('rekognition', region_name = 'us-west-2')

        response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': key_name}})

        textDetections = response['TextDetections']

        # NLP by AWS Comprehend
        words = []
        for text in textDetections:
            words.append(text['DetectedText'])

        # the words are replicated and need cutting
        text = ' '.join(words)
        text = text.split()
        num = int(len(text) / 2)
        words = text[0:num]
        text = ' '.join(text[0:num])

        return text

@application.route('/upload_page', methods=['POST', 'GET'])
def upload_page():
    return render_template('upload_page.html')

@application.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
    # get the image uploaded by the user
        file = request.files['file']
        # bucket = 'ucb-rekognition'
        bucket = 'handwritten-image'
        # create a resource of S3 to use 'Bucket' attribute
        s3_resource = boto3.resource('s3')

        # upload the file as on object using put_object
        s3_resource.Bucket(bucket).put_object(Key=file.filename, Body=file)

        ## detect text from the image uploaded onto S3 by AWS Rekognition
        rekognition = boto3.client('rekognition', region_name = 'us-west-2')

        response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': file.filename}})

        textDetections = response['TextDetections']

        # NLP by AWS Comprehend
        words = []
        for text in textDetections:
            words.append(text['DetectedText'])

        # the words are replicated and need cutting
        text = ' '.join(words)
        text = text.split()
        num = int(len(text) / 2)
        words = text[0:num]
        text = ' '.join(text[0:num])

        comprehend = boto3.client("comprehend", region_name='us-west-2')
        language = 'en'

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


        return render_template("rekognition.html", words=words, score_phrase=score_phrase, phrases=phrases, length=length, score_sentiment=score_sentiment, category=category)



if __name__ == '__main__':
    application.run(debug=True)
