"""
Author: Miles Catlett
1/9/2023
This python file lists the functions to connect to caspio.
"""

import requests
import db
import json

# Credentials are inserted in a MYSQL database and retrieved with an id
aid = '1'

# This data is found in the credentials file
access_token = db.get_token()
caspio = db.get_caspio_creds(aid)
account = caspio[0]
client_id = caspio[1]
client_secret = caspio[2]
body = 'grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}


def get_new_token():
    """
    This function gets a new token to be able to call the other functions, using user credentials. Data is posted to
    the MYSQL database.
    :return: Dictionary
    """
    response = requests.get('https://' + account + '.caspio.com/oauth/token', data=body)
    token_values = response.json()
    access_token = token_values['access_token']
    token_type = token_values['token_type']
    expires_in = token_values['expires_in']
    refresh_token = token_values['refresh_token']
    db.add_token(access_token, token_type, expires_in, refresh_token)


def get_app_list():
    """
    This function gets a list of apps from the caspio app and then appends the data to a string.
    :return: String
    """
    response = requests.get('https://' + account + '.caspio.com/rest/v2/applications', headers=headers)
    msg = ''
    json = response.json()
    for i in range(len(json['Result'])):
        msg += json['Result'][i]['AppName'] + '<br />'
    return msg


def get_table_fields(table_name):
    """
    This function gets a list of table names from caspio.
    :param table_name: String
    :return: List
    """
    response = requests.get('https://' + account + '.caspio.com/rest/v2/tables/' + table_name + '/fields',
                            headers=headers)
    json = response.json()
    field_list = []
    for i in range(len(json['Result'])):
        field_list.append(json['Result'][i]['Name'])
    return field_list


def insert_record(table_name, records):
    """
    This function posts a user table and the records to be added to the caspio table, and then a message is returned.
    :param table_name: String
    :param records: String
    :return: String
    """
    fields = get_table_fields(table_name)
    data = {fields[j]: records[j] for j in range(len(fields))}
    data = json.dumps(data)
    requests.post('https://' + account + '.caspio.com/rest/v2/tables/' + table_name + '/records', data=data,
                  headers=headers)
    msg = 'Success!'
    return msg
