import RPi.GPIO as GPIO
import boto3
import time
from logger import insert_logs


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

# Configure Variables
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


def check_status():  # Log Status
    global Status
    global StatusCheck
    global Message_To_Send

    if Status == 1 and StatusCheck == 0 or Status == 1 and StatusCheck == 2:
        # Log Status as Closed
        lt = "Status Change"
        st = "The Garage Door Is Closed"
        im = "None"
        ra = "None"
        insert_logs(lt,st,im,ra)  # insert into database
        StatusCheck = Status
    if Status == 0 and StatusCheck == 1:
        # Log Status as Open
        lt = "Status Change"
        st = "The Garage Door Is Open"
        im = "None"
        ra = "None"
        insert_logs(lt, st, im, ra)  # insert into database
        # Take a Photo TBD
        Message_To_Send = "Garage Door Is Open!"
        StatusCheck = 2
    if Status == 0:
        if StatusCheck == 0:
            lt = "Status Change"
            st = "The Garage Door was Open on Startup"
            im = "None"
            ra = "None"
            insert_logs(lt, st, im, ra)  # insert into database
            # Take a Photo
            StatusCheck = 2
        if StatusCheck == 2:
            return None
    return StatusCheck, Message_To_Send


def opened():  # Update Status when Door_Switch Reads Open
    global Status
    Status = 1
    check_status()
    return Status


def closed():  # Update Status when Door_Switch Reads Closed
    global Status
    Status = 0
    check_status()
    return Status


def sleep():  # Setup a sleep time for the loop
    time.sleep(.5)
    return


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