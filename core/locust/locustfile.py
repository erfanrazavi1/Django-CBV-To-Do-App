from locust import HttpUser, task


class MyUser(HttpUser):
    def on_start(self):

        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            data={"username": "erf1", "password": "hasaniii1234"},
        ).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access', None)}"
        }

    @task
    def todo_list(self):
        self.client.get("/api/v1/todo/")
