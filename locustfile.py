from locust import HttpUser, task, between

class StructuralInferenceUser(HttpUser):
    wait_time = between(1, 3) 

    @task
    def submit_image(self):
        files = {'file': ('test_crack.jpg', b'dummy_byte_data', 'image/jpeg')}
        self.client.post("/analyze/crack-detection", files=files)