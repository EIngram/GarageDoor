# Log events to database
import os
import sqlite3
import datetime, time

Base_DIR = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(Base_DIR + '\logs', "garage_logs.db")  # change \ to / on raspberry pi
DataTable = "events"
lt = ""
st = ""
im = ""
ra = ""
last_db_status = ""

FNAME = datetime.date.today()
FTIME = str(time.strftime('%I:%M %p'))


def insert_logs(lt,st,im,ra):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO events(LogType, Status, Image, RequestAddress, Date, Time)
                          VALUES(?,?,?,?,?,?)''', (lt, st, im, ra, str(FNAME), str(FTIME)))
    conn.commit()
    conn.close()


def last_db_status():
    global last_status
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT Status Date, Time from events WHERE LogType = 'Status Change' ORDER BY id DESC LIMIT 1")
    last_db_status = cursor.fetchone()
    last_db_status = str(last_db_status[0])
    conn.close()
    return last_db_status
