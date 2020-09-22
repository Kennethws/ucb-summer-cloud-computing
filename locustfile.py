from locust import HttpUser, TaskSet, between, task

class UserBehavior(TaskSet):
	@task
	def submit(self):
			self.client.post('/', {'username': 'Kobe Bryant is the best NBA player.', 'password': 'en'})
	
	@task	
	def get_boto(self):
			self.client.get('/boto')

class WebsiteUser(HttpUser):
	tasks = [UserBehavior]
	wait_time = between(1, 2)