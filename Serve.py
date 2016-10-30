#!flask/bin/python
from flask import Flask, jsonify, request
from Credentials import ip_addy
from logger import last_db_status, insert_logs


app = Flask(__name__)


@app.route('/DoorStatus', methods=['GET'])
def get_status():
    lt = "Web or Echo Request"
    st = "Status Check"
    im = "None"
    ra = request.environ['REMOTE_ADDR']
    insert_logs(lt, st, im, ra)  # Log the request to the datebase
    Status = {}
    Status["Status"] = str(last_db_status())  # get the last status change from the database and serve it
    return jsonify({'Door': Status})

if __name__ == '__main__':
    app.run(host=ip_addy, debug=False)
