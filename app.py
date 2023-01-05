import os
from flask import Flask, request, render_template
import func

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


@app.route('/caspio-get-token-231656231546299648941656', methods=['GET'])
def token():
    if request.method == 'GET':
        func.get_new_token()
        msg = "Success!"
    return render_template('token.html', msg=msg)


@app.route('/caspio-get-app-list-231651546299648946', methods=['GET'])
def applist():
    if request.method == 'GET':
        msg = func.get_app_list()
    return render_template('token.html', msg=msg)


@app.route('/caspio-insert-record-3784659101', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        msg = func.insert_record('Appointments', ['Chad', 'Jim', '12/29/2022'])
    return render_template('token.html', msg=msg)


application = app