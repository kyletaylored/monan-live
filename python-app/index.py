# from gpiozero import MotionSensor
# from gpiozero import PiCamera
import base64
import datetime
import json
import os
import pathlib
import pprint
import random
import sys

import requests
# Load environmental variables
from dotenv import load_dotenv

load_dotenv()

# Set up printer and text generator
pp = pprint.PrettyPrinter(indent=4)
f = open('phrases.json')
phrases = json.load(f)
f.close()
phrase = random.choice(phrases['data'])

# Get Drupal host and global auth
global url
url = os.getenv('DRUPAL_HOST', 'https://live-monan-live.pantheonsite.io')
global drupal_auth

# Authenticate with Drupal site
auth_data = {
    'name': os.getenv('DRUPAL_USER', 'superuser'),
    'pass': os.getenv('DRUPAL_PASS', 'password'),
}
auth_string = auth_data['name'] + ":" + auth_data['pass']

# Create object for PIR sensor
# PIR sensor is connected to GPIO-4 (pin 7)
# pir = MotionSensor(4)

# Create Object for PiCamera
# camera = PiCamera()


# Create filename from date and time.
def get_file_name():
    now = datetime.datetime.now()
    f_name = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")
    return f_name


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def monan_auth():
    # See if we're logged in
    session_request = requests.get(url + '/session/token')
    if session_request.status_code == 200 and session_request.text is not None:
        # We're logged in, return the token
        return session_request.text

    # Make request, get back CSRF and logout tokens.
    auth_request = requests.post(url + '/user/login?_format=hal_json', data=auth_data)
    drupal_auth = auth_request.json()

    # Check if session is already open
    if auth_request.status_code == 403:
        if drupal_auth['message'] == "This route can only be accessed by anonymous users.":
            # Get new session token
            session_request = requests.get(url + '/session/token')
            return session_request.text

    # Return session token
    return drupal_auth['csrf_token']


def monan_file(f_name):
    # Get base64 image
    # image_data = get_base64_encoded_image(filename)
    # image_extension = pathlib.Path(filename).suffix
    image_name = pathlib.Path(f_name).name

    # Prepare data for POST
    file = open(f_name, "rb")
    binary_data = file.read()
    file.close()

    # Headers
    headers = {
        "Content-Type": "application/octet-stream",
        "Accept": "application/vnd.api+json",
        "Content-Disposition": 'file; filename="' + image_name + '"',
        "X-CSRF-Token": monan_auth(),
        "Authorization": "Basic " + base64.b64encode(auth_string.encode('utf-8')).decode('utf-8'),
    }
    image_response = requests.post(url + '/jsonapi/node/article/field_image', data=binary_data, headers=headers)
    return image_response


def send_to_monan_live(f_name):
    # Upload image.
    image_response = monan_file(f_name)
    pp.pprint(image_response.json())

    # Prepare article data.
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "X-CSRF-Token": monan_auth(),
        "Authorization": "Basic " + base64.b64encode(auth_string.encode('utf-8')).decode('utf-8'),
    }
    data = json.dumps({
        "data": {
            "type": "node--article",
            "attributes": {
                "title": "Mike: " + phrase['phrase'],
                "body": {
                    "value": phrase['meaning'],
                    "format": "plain_text"
                }
            },
            "relationships": {
                "field_image": {
                    "data": {
                        "type": "file--file",
                        "id": image_response.json()['data']['id'],
                    }
                }
            }
        }
    })

    # Create new node
    article_response = requests.post(url + '/jsonapi/node/article', data=data, headers=headers)
    pp.pprint(article_response.json())


# Test
send_to_monan_live('/Users/kyletaylor/Downloads/monan-small.png')
sys.exit()

# Run main
while True:
    # Get filename, set to tmp
    filename = get_file_name()

    # Wait for motion to be detected
    pir.wait_for_motion()
    print("Mike alert!")

    # Wait 2 seconds
    time.sleep(2)

    # Preview camera on screen until picture is taken
    # Only used if using desktop OS.
    # camera.start_preview()

    # Take picture, save to temp
    print("Taking photo: " + filename)
    path_to_file = '/tmp/' + filename
    camera.capture(path_to_file)
    # camera.stop_preview()

    # Send to monan.live
    send_to_monan_live(path_to_file)

    # Clean files up
    os.remove(path_to_file)

    # Wait 10 seconds before checking the motion sensor again.
    time.sleep(10)
