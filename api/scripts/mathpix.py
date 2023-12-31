#!/usr/bin/env python3

import os
import base64
import requests
import json
from dotenv import load_dotenv

#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py 
#

load_dotenv()

app = os.getenv('MATHPIX_APP_ID')
key = os.getenv('MATHPIX_APP_KEY')

default_headers = {
    'app_id': app,
    'app_key': key,
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/text'
service_pdf = 'https://api.mathpix.com/v3/pdf'

#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

#
# Return the base64 encoding of an image with the content.
#
def image_content(contents):
    encoded_string = base64.b64encode(contents).decode()
    return f"data:image/jpg;base64,{encoded_string}"

#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)

#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def pdf(args, headers=default_headers, timeout=30):
    r = requests.post(service_pdf,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)
