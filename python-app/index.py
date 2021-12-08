from gpiozero import MotionSensor
# from gpiozero import PiCamera
import requests
from requests.auth import HTTPBasicAuth
import time
import datetime
import os
import base64
import pathlib


# Load environmental variables
from dotenv import load_dotenv
load_dotenv()

# Get Drupal host and global auth
global url
url = os.getenv('DRUPAL_HOST', 'https://live-monan-live.pantheonsite.io')
global drupal_auth

# Create object for PIR sensor
# PIR sensor is connected to GPIO-4 (pin 7)
# pir = MotionSensor(4)

# Create Object for PiCamera
# camera = PiCamera()

# Create filename from date and time.
def getFileName():
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")
    return filename

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def monan_auth():
    # Authenticate with Drupal site
    auth_data = {
        'name': os.getenv('DRUPAL_USER', 'superuser'),
        'pass': os.getenv('DRUPAL_PASS', 'password'),
    }

    # Make request, get back CSRF and logout tokens.
    auth_request = requests.post(url + '/user/login?_format=hal_json', data=auth_data)
    drupal_auth = auth_request.json()

    # Check if session is already open
    if auth_request.status_code == 403:
        if drupal_auth['message'] == "This route can only be accessed by anonymous users.":
            # Get new session token
            session_request = requests.get(url + '/session/token')
            return session_request.text()
    
    # Return session token
    return drupal_auth['csrf_token']


def monan_file(filename):

    # Get base64 image
    image_data = get_base64_encoded_image('/tmp/' + filename)
    image_extension = pathlib.Path(filename).suffix.lstrip(1)

    # Prepare data
    request_data = {
        "data": {
        "type": "file--file",
        "attributes": {
            "filename": [
                {
                    "value": filename
                }
            ],
            "filemime": {
                "value": "image/" + image_extension
            },
            "uri": [
                {
                    "value": "public://" + filename
                }
            ],
            "type": {
                "target_id": "file"
            },
            "data": [
                {
                    "value": image_data
                }
            ]
        }
        }
    }

    requests.post(url, data=request_data)


    # Send request
    r = requests.post('https://httpbin.org/post', data={'key': 'value'})

def send_to_monan_live(filename):
    # do something
    a = 1

# Run main
while True:
    # Get filename, set to tmp
    filename = getFileName()

    # Wait for motion to be detected
    pir.wait_for_motion()
    print("Mike alert!")

    # Wait 2 seconds
    time.sleep(2);
    
    # Preview camera on screen until picture is taken
    # Only used if using desktop OS.
    # camera.start_preview()

    # Take picture, save to temp
    print("Taking photo: " + filename)
    camera.capture('/tmp/' + filename)
    # camera.stop_preview()

    # Send to monan.live
    send_to_monan_live(filename)

    # Clean files up
    os.remove(filename)

    # Wait 10 seconds before checking the motion sensor again.
    time.sleep(10)