import requests
import db
import json

# Insert the id to the creds here:
aid = '1'

access_token = db.get_token()
caspio = db.get_caspio_creds(aid)
account = caspio[0]
client_id = caspio[1]
client_secret = caspio[2]
body = 'grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}


def get_new_token():
    response = requests.get('https://' + account + '.caspio.com/oauth/token', data=body)
    token_values = response.json()
    access_token = token_values['access_token']
    token_type = token_values['token_type']
    expires_in = token_values['expires_in']
    refresh_token = token_values['refresh_token']
    db.add_token(access_token, token_type, expires_in, refresh_token)


def get_app_list():
    response = requests.get('https://' + account + '.caspio.com/rest/v2/applications', headers=headers)
    msg = ''
    json = response.json()
    for i in range(len(json['Result'])):
        msg += json['Result'][i]['AppName'] + '<br />'
    return msg


def get_table_fields(table_name):
    response = requests.get('https://' + account + '.caspio.com/rest/v2/tables/' + table_name + '/fields',
                            headers=headers)
    json = response.json()
    field_list = []
    for i in range(len(json['Result'])):
        field_list.append(json['Result'][i]['Name'])
    return field_list


def insert_record(table_name, records):
    fields = get_table_fields(table_name)
    data = {fields[j]: records[j] for j in range(len(fields))}
    data = json.dumps(data)
    requests.post('https://' + account + '.caspio.com/rest/v2/tables/' + table_name + '/records', data=data,
                  headers=headers)
    msg = 'Success!'
    return msg
