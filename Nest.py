# https://pypi.python.org/pypi/python-nest/2.9.1
# Function to update nest status to Home when garage door is opened
# pip install python-nest
import nest

User = ''  # Enter email address here or store in a config
Pass = ''  # Enter your password or store in a config

N = nest.Nest(User, Pass)


for structure in N.structures:
    structure.away = False
