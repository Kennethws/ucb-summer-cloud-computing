from locust import HttpUser, TaskSet, between, task, SequentialTaskSet

class UserBehavior(SequentialTaskSet):

	@task
	def submit(self):
			self.client.post('/', {'text': 'Kobe Bryant is the best NBA player.', 'language': 'en'})
	
	@task	
	def get_boto(self):
			self.client.get('/boto')

class WebsiteUser(HttpUser):
	tasks = [UserBehavior]
	host = "http://boto3-env.eba-8zj3bgu3.us-west-2.elasticbeanstalk.com/"
	wait_time = between(1, 2)