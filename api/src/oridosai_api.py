import json
import time

import requests


class OridosAIAPI:
    def __init__(self, api_url, data, image_file_path):
        self.api_url = api_url
        self.data = data
        self.image_file_path = image_file_path
        self.retry_count = 3
        self.retry_delay = 5  # seconds

    def send_request(self):
        """Sends a POST request to the specified URL with the provided data."""
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(self.data))
            if response.status_code == 200:
                return response
            else:
                raise Exception(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"An error occurred while sending the request: {e}")

    def download_image(self, image_url):
        """
        Downloads the image from the given URL with retries.
        """
        for attempt in range(self.retry_count):
            try:
                with open(self.image_file_path, "wb") as file:
                    file.write(image_url)
                print("Image downloaded successfully.")
                return
            except Exception as e:
                print(f"An error occurred while downloading the image: {e}")

            print(f"Retrying... ({attempt + 1}/{self.retry_count})")
            time.sleep(self.retry_delay)

        raise Exception("Failed to download the image after retries.")

    def execute(self):
        """Executes the process of sending the request and downloading the image."""
        response = self.send_request()
        if response.content:
            self.download_image(response.content)
        else:
            raise Exception("Image URL not found in the response.")
