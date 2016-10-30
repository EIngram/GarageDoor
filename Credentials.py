# Used to store credentials for AWS & Nest
# Can update to store as environmental variable or
# store in /etc/boto.cfg
# Setup a monthly spend limit for AWS

#
# -----------AWS Credentials for SNS-----------------------------------
#
ACCESS = ''  # AWS_Access_Key
SECRET = ''  # AWS_Secret_Key
TOPIC = ''  # AWS Topic for SMS Message. Needs to contain all 6 Segment
REGION = 'us-east-1'  # Enter your AWS Region

#
# ----------Nest Credentials-------------------------------------------
#
User = '123'  # Nest Account Email Address
Pass = 'Test'  # Nest Account Password

#
# ----------Configurations for Echo support-----------------------------
#
ip_addy = "192.168.1.193"  # set your device IP (should be static) here

