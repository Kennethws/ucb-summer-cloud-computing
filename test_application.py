from flask import Flask, render_template, request
import boto3

def test():

    test_application = Flask(__name__)

    @test_application.route('/boto', methods = ['POST', 'GET'])
    def text_detect():
        if request.method == 'POST':
            comprehend = boto3.client('comprehend', region_name='us-west-2')
            text = 'Kobe Bean Bryant (/ˈkoʊbiː/ KOH-bee; August 23, 1978 – January 26, 2020) was an American professional basketball player. A shooting guard, he spent his entire career with the Los Angeles Lakers in the National Basketball Association (NBA).'
            language = 'en'
            result = comprehend.detect_key_phrases(Text = text, LanguageCode = language)
            
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

    
    @test_application.route('/upload', methods = ['POST'])
    def upload():
        if request.method == 'POST':
            bucket = 'ucb-rekognition'
            rekognition = boto3.client('rekognition', region_name='us-west-2')
            response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': 'test.PNG'}})
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
        test_application.run(host='0.0.0.0', port=8080, debug=True)