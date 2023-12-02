from locust import HttpUser, task, TaskSet


class MainBehavior(TaskSet):
    @task
    def main_task(self):
        self.client.get("/mocking_analyze")


class LocustUser(HttpUser):
    host = "http://0.0.0.0:8000"
    tasks = [MainBehavior]
