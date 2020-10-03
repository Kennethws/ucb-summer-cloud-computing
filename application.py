from flask import Flask, render_template, request, redirect, url_for
import boto3

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

@application.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
    # get the image uploaded by the user
        file = request.files['file']
        bucket = 'ucb-rekognition'
        
        # create an S3 client
        s3_client = boto3.client('s3')
        
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
        # return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
