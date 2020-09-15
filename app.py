import boto3

comprehend = boto3.client("comprehend")

text = input("Please enter a message:")

print(comprehend.detect_key_phrases(Text = text, LanguageCode = 'en'))