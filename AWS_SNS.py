import boto3
import time
# setup AWS SNS
# Create a Topic and add subscribers
# Highly suggest you cap your monthly spending for SNS in case something goes wrong
# Get keys for User, store below (or store in /etc/boto.cfg)

ACCESS = ''
SECRET = ''
REGION = 'us-east-1'
Message_To_Send = ""
ct = str(time.strftime('%I:%M %p'))


def IsOpen():  # Alert when Door has been open too long
    Message_To_Send = ('Garage Door Is Open. ' + str(ct))
    publish()


def NightlyCheck(Status):  # Send nightly SMS message with current status are predetermined time
    Message_To_Send = ('Garage Door Is ' + str(Status) + '.' + str(ct))
    publish()


def publish():
    c = boto3.client(
        'sns',
        region_name=REGION,
        aws_access_key_id=ACCESS,
        aws_secret_access_key=SECRET
    )

    c.publish(
        TopicArn='arn:aws:sns:us-east-1:458816371970:GarageDoor',  # Your TopicARN from AWS
        Message=Message_To_Send
    )

