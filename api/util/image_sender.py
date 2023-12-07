import requests
import scripts.mathpix as mathpix
import json

class ImageSender:
    """
    Send an image to MathPIX
    """
    def __init__(self, url):
        """
        Initialize the ImageSender with a specific URL.

        Parameters:
        url (str): The URL to which the image will be sent.
        """
        self.url = url

    def send_image(self, image_path):
        """
        Send an image to the initialized URL and print the response.

        Parameters:
        image_path (str): The file path of the image to be sent.
        """
        headers = {
            "accept": "application/json"
        }

        with open(image_path, "rb") as img:
            file_payload = {"file": (image_path, img, "image/jpeg")}
            response = mathpix.latex({
                'src': mathpix.image_uri(image_path), #mathpix.image_uri('./api/images/algebra.jpg'),
                'ocr': ['math', 'text'],
                'formats': ['text', 'latex_styled', 'asciimath', 'mathml', 'latex_simplified'],
                'format_options': {
                    'text': {
                        'transforms': ['rm_spaces', 'rm_newlines'],
                        'math_delims': ['$', '$']
                    },
                    'latex_styled': {'transforms': ['rm_spaces']}
                }
            })
            # response = requests.post(self.url, headers=headers, files=file_payload)
            print(f"response is: {json.dumps(response, indent=4, sort_keys=True)}")
        #     # Check and print the response
        #     if response.status_code == 200:
        #         print("Success:", response.json())
        #     else:
        #         print("Error:", response.text)

        # return response.text