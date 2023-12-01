from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/test")
