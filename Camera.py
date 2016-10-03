# install picamera
import picamera
import time
import datetime
import os.path

FNAME = datetime.date.today()
FTIME = str(time.strftime('%I:%M %p'))
SavePath = 'photos'
SaveName = os.path.join(SavePath, str(FNAME) + '|' + str(FTIME) + '.jpg')


with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.start_preview()
    time.sleep(2.5)
    camera.capture(SaveName)
    camera.close()
