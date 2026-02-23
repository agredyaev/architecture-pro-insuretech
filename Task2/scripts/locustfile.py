from locust import HttpUser, between, task


class ScalabilityUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_root(self) -> None:
        self.client.get("/")
