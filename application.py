from flask import Flask, render_template, request
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

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
