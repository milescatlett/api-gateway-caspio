import mysql.connector
from datetime import datetime
import cr

hostname = cr.hostname
username = cr.username
password = cr.password
database = cr.database


def get_token():
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute("SELECT access_token FROM token_values ORDER BY tid DESC")
    data = cur.fetchall()
    conn.close()
    return data[0][0]


def add_token(access_token, token_type, expires_in, refresh_token):
    timestamp = datetime.today()
    tid = get_tid()
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    stmt = (
        "INSERT INTO token_values (access_token, token_type, expires_in, refresh_token, timestamp, tid) VALUES (%s, %s, %s, %s, %s, %s)")
    data = (access_token, token_type, expires_in, refresh_token, timestamp, tid)
    cur.execute(stmt, data)
    conn.commit()
    conn.close()


def get_tid():
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute("""SELECT tid FROM token_values ORDER BY tid DESC""")
    data = cur.fetchall()
    conn.close()
    return int(data[0][0]) + 1


def get_caspio_creds(aid):
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    query = "SELECT account, client_id, client_secret FROM caspio_creds WHERE aid = %s"
    aid = (aid,)
    cur.execute(query, aid)
    data = cur.fetchall()
    conn.close()
    return data[0]