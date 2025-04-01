from locust import HttpUser, task, between

class ShortenerUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def shorten_url(self):
        self.client.post("/links/shorten", json={
            "original_url": "https://example.com/" + str(hash(self))
        })
    
    @task(3)
    def access_short_url(self):
        self.client.get("/abc123")  # Assuming this short code exists