"""
Author: Miles Catlett
1/9/2023
The purpose of this app is to create an API Gateway example/demo posting to a no code platform called
Caspio.
"""

import os
from flask import Flask, request, render_template
import func

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


@app.route('/caspio-get-token-231656231546299648941656', methods=['GET'])
def token():
    """
    Route to renew a token. Set with chron job to activate route and get new token every 12 hours.
    :return: None
    """
    if request.method == 'GET':
        func.get_new_token()
        msg = "Success!"
    return render_template('token.html', msg=msg)


@app.route('/caspio-get-app-list-231651546299648946', methods=['GET'])
def applist():
    """
    Route for retrieving a list of apps from the caspio account.
    :return: None
    """
    if request.method == 'GET':
        msg = func.get_app_list()
    return render_template('token.html', msg=msg)


@app.route('/caspio-insert-record-3784659101', methods=['GET', 'POST'])
def insert():
    """
    Route for posting a row of data to a caspio table.
    :return: None
    """
    if request.method == 'GET':
        msg = func.insert_record('Appointments', ['Chad', 'Jim', '12/29/2022'])
    return render_template('token.html', msg=msg)


application = app