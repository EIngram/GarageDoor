# Log events to database
import os
import sqlite3
import datetime, time

Base_DIR = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(Base_DIR + '\logs', "garage_logs.db")  # Use this while working in Windows Environment
# db = os.path.join(Base_DIR + '/logs', "garage_logs.db")  # use this while running on the PI
DataTable = "events"
lt = ""
st = ""
im = ""
ra = ""
last_db_status = ""
FNAME = ""
FTIME = ""

def current_time():
    global FTIME
    global FNAME
    FNAME = datetime.date.today()
    FTIME = str(time.strftime('%I:%M %p'))
    return FNAME, FTIME

def insert_logs(lt,st,im,ra):
    current_time()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO events(LogType, Status, Image, RequestAddress, Date, Time)
                          VALUES(?,?,?,?,?,?)''', (lt, st, im, ra, str(FNAME), str(FTIME)))
    conn.commit()
    conn.close()


def last_db_status():
    global last_db_status
    current_time()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT Status Date, Time from events WHERE LogType = 'Status Change' ORDER BY id DESC LIMIT 1")
    last_db_status = cursor.fetchone()
    last_db_status = str(last_db_status[0]) + ' as of ' + str(last_db_status[1])  # + ' On ' + str(last_db_status[2])
    conn.close()
    return last_db_status
