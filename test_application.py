# test boto3 connection and boto.html
from flask import Flask, render_template
import boto3

test_application = Flask(__name__)

@test_application.route('/')
def text_detect():
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    text = 'Kobe Bean Bryant (/ˈkoʊbiː/ KOH-bee; August 23, 1978 – January 26, 2020) was an American professional basketball player. A shooting guard, he spent his entire career with the Los Angeles Lakers in the National Basketball Association (NBA).'
    language = 'en'
    result = comprehend.detect_key_phrases(Text = text, LanguageCode = language)
    return render_template('boto.html', result = result)

if __name__ == '__main__':
    test_application.run(host='0.0.0.0', port=8080, debug=True)
    
    