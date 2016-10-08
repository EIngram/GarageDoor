# https://pypi.python.org/pypi/python-nest/2.9.1
# Function to update nest status to Home when garage door is opened
# pip install python-nest
import nest
from Credentials import User, Pass

# User = ''  # Enter email address here or store in a config
# Pass = ''  # Enter your password or store in a config
status = None
N = nest.Nest(User, Pass)


def is_home():  # set status to Home
    for structure in N.structures:
        structure.away = False


def go_away():  # set status to Away
    for structure in N.structures:
        structure.away = True


def nest_status():  # get current status from nest. True = Away, False = Home
    global status
    for structure in N.structures:
        status = structure.away
        return status
