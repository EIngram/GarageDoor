# pip install boto3
# setup AWS SNS
# Create a Topic and add subscribers
# Highly suggest you cap your monthly spending for SNS in case something goes wrong
# Get keys for User, store in Credentials.py (or store in /etc/boto.cfg)
import boto3
import time
from Credentials import ACCESS, REGION, SECRET, TOPIC


message_to_send = ""
ct = str(time.strftime('%I:%M %p'))


def is_open():  # Alert when Door has been open too long
    message_to_send = ('Garage Door Is Open. ' + str(ct))
    publish()


def nightly_check(Status):  # Send nightly SMS message with current status are predetermined time
    message_to_send = ('Garage Door Is ' + str(Status) + '.' + str(ct))
    publish()


def publish():
    c = boto3.client(
        'sns',
        region_name=REGION,
        aws_access_key_id=ACCESS,
        aws_secret_access_key=SECRET
    )

    c.publish(
        TopicArn=TOPIC,  # Your TopicARN from AWS
        Message=message_to_send
    )
