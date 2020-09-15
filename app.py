import boto3

comprehend = boto3.client("comprehend")

text = input("Please enter a message:")
language = input("Please enter your language:")

print(comprehend.detect_key_phrases(Text = text, LanguageCode = language))