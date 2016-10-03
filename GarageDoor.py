import RPi.GPIO as GPIO
import boto3
import time
import picamera

# ----------------------------------------- Configurations -------------------------------------------------------------

# Turn off Warning Messages & Set configs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
Status = 0
StatusCheck = 0

# Configure GPIO PINS
Door_Switch = 5
Solenoid = 3
# Motion_Sensor =

# Configure GPIO Settings
GPIO.setup(Door_Switch, GPIO.IN)
GPIO.setup(Solenoid, GPIO.OUT, initial=GPIO.HIGH)
# GPIO.setup(Motion_Sensor, GPIO.IN)

# Configure AWS for SMS
REGION = 'us-east-1'  # input your AWS region
ACCESS = ''  # Access Key
SECRET = ''  # Secret Key
Message_To_Send = ""
Message_Counter = 0

# ----------------------------------------- End Configurations ---------------------------------------------------------
#
# ----------------------------------------- Functions ------------------------------------------------------------------


def blink(Solenoid):  # testing only
    GPIO.output(Solenoid, GPIO.LOW)
    time.sleep(.1)
    GPIO.output(Solenoid, GPIO.HIGH)
    time.sleep(.1)
    return


def trigger(Solenoid):  # Open and Close the Door
    GPIO.output(Solenoid, GPIO.LOW)  # Close the Relay
    time.sleep(.2)
    GPIO.output(Solenoid, GPIO.HIGH)  # Open the Relay


def log():  # Log Status
    global Status
    global StatusCheck
    global Message_To_Send

    if Status == 1 and StatusCheck == 0 or Status == 1 and StatusCheck == 2:
        print("Garage is Closed")  # Log Status Change
        StatusCheck = Status
    if Status == 0 and StatusCheck == 1:
        print("Garage is Open, Sending SMS")  # Log Status Change | Take Photo
        Message_To_Send = "Garage Door Is Open!"
        StatusCheck = 2
        SMS()
    if Status == 0:
        if StatusCheck == 0:
            print("Garage was open on Startup")  # Log Status Change
            StatusCheck = 2
        if StatusCheck == 2:
            return None
    return StatusCheck, Message_To_Send


def opened():  # Update Status when Door_Switch Reads Open
    global Status
    Status = 1
    log()
    return Status


def closed():  # Update Status when Door_Switch Reads Closed
    global Status
    Status = 0
    log()
    return Status


def sleep():  # Setup a sleep time for the loop
    time.sleep(.5)
    return


def SMS():  # Send a Text Message
    global Message_To_Send
    global Message_Counter

    if Message_Counter < 2:
        c = boto3.client(
            'sns',
            region_name=REGION,
            aws_access_key_id=ACCESS,
            aws_secret_access_key=SECRET
        )
        c.publish(
            PhoneNumber='',  # Your phone number here +19871235555
            Message=Message_To_Send
            )
        Message_Counter += 1
        print(Message_Counter)
        return Message_Counter

# ----------------------------------------- End Functions --------------------------------------------------------------
#
# ---------------------------------------------- Main ------------------------------------------------------------------

while True:
    if GPIO.input(Door_Switch) == GPIO.LOW:  # Garage Door Sensor indicates opened
        opened()
        sleep()
    else:  # Garage Door Sensor indicates closed
        closed()
        for i in range(0, 1):
           blink(Solenoid)
        sleep()
GPIO.cleanup()