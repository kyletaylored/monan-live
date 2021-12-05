from gpiozero import MotionSensor
from gpiozero import PiCamera
import time
import datetime

# Create object for PIR sensor
# PIR sensor is connected to GPIO-4 (pin 7)
pir = MotionSensor(4)

# Create Object for PiCamera
camera = PiCamera()

# Create filename from date and time.
def getFileName():
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")
    return filename

while True:
    # Get filename
    filename = getFileName()

    # Wait for motion to be detected
    pir.wait_for_motion()
    print("Mike alert!")
    
    # Preview camera on screen until picture is taken
    camera.start_preview()

    # Take picture
    print("Taking photo: " + filename)
    camera.capture(filename)
    camera.stop_preview()

    # Wait 10 seconds before taking another picture
    time.sleep(10)