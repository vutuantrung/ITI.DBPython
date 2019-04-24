import sqlite3 
from sqlite3 import Error
from privateData import dbPath, datPath

def create_connection(db_file):
    """ Create a database connection to a SQLite database""" 
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return None

def read_source_data():
    try:
        with open(datPath, 'r') as file:
            return file
    except Error as e:
        print(e)
    """
    with open(datPath, 'r') as file:
        for line in file:
            print(line)
    """
    return None

def main():
    conn = create_connection(dbPath)
    return None

