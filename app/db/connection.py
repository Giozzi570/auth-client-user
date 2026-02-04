import sqlite3


def get_connection(data_base_user):
    conn = sqlite3.connect(data_base_user)
    return conn