from locust import HttpUser, TaskSet, between, task, SequentialTaskSet, User

class UserBehavior(TaskSet):
	@task
	def submit(self):
			self.client.post('/', {'Text': 'Kobe Bryant is the best NBA player.', 'Language': 'en'})
	
	@task	
	def get_boto(self):
			self.client.get('/boto')

class WebsiteUser(HttpUser):
	tasks = [UserBehavior]
	wait_time = between(1, 2)