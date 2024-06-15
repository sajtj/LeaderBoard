from locust import HttpUser, task

class TestUser(HttpUser) :
    @task
    def test_user(self) :
        self.client.get("api/prediction/usersleaderboard/1/")