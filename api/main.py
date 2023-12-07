import io
import os
import sys

# Get the current script's directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project root path
project_root = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Append the project root and current script directory to the system path
sys.path.append(project_root)
sys.path.append(current_script_directory)

from fastapi import Depends, FastAPI, File, Response, UploadFile
from starlette.responses import RedirectResponse
from starlette.status import HTTP_201_CREATED

from PIL import Image
import scripts.mathpix as mathpix
import json

# Create a FastAPI application
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


# Define a route to handle the root endpoint and redirect to the API documentation
@app.get("/")
async def root():
    return RedirectResponse(app.docs_url)

@app.post("/img2txt", status_code=HTTP_201_CREATED)
async def i2t(file: UploadFile = File(...)):
    contents = await file.read()

    r = mathpix.latex({
        'src': mathpix.image_content(contents), #mathpix.image_uri('./api/images/algebra.jpg'),
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

    print(json.dumps(r, indent=4, sort_keys=True))
    # assert(r['latex_simplified'] == '12 + 5 x - 8 = 12 x - 10')

    return {"result": json.dumps(r, indent=4, sort_keys=True)}

@app.post("/img2txt_url", status_code=HTTP_201_CREATED)
async def i2t(image_path: str):
    r = mathpix.latex({
        'src': image_path,
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

    print(json.dumps(r, indent=4, sort_keys=True))
    # assert(r['latex_simplified'] == '12 + 5 x - 8 = 12 x - 10')

    return {"result": json.dumps(r, indent=4, sort_keys=True)}
