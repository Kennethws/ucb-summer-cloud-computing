# UCB Cloud Computing
This is an NLP project that creates a flask web app which is structured by AWS CodePipeline. Users can pass in text messages with its language type to detect key phrases and to do sentiment analysis. The whole app is has the property of continuous integration (CI) and continuous delivery (CD), which means it is auto-linted, auto-tested, and auto-deployed. It takes care of cyber-security, load-balancing, and monitoring as well.

Here is the link to our web app: http://boto3-env.eba-8zj3bgu3.us-west-2.elasticbeanstalk.com/

## Procedures (Code Pipeline)
1. Source: Github (Flask + AI API - AWS Comprehend)
2. Linting + Testing: CodeBuild
3. Deploy: Elastic Beanstalk
4. Load Test: Locust

## Source
We store our source code in Github which is cloned to our AWS Cloud9 instances. 

Add an SSH key to our Github account
```
ssh-keygen -t rsa
```
