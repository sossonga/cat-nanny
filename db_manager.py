from datetime import datetime, timedelta
import json
from pathlib import Path
import sqlite3
import time
import catnanny


DB_FILE_PATH = Path('cat-nanny.db')
SCHEMA_PATH = Path('schema.sql')
USER_ACCOUNTS_PATH = Path('user_accounts.json')

SENSOR_POLL_DELAY = 5

DB_CLEAN_DURATION = timedelta(hours=3)
DB_CLEAN_MAX_RECORDS = 10000


def _get_db_connection():
    """The _get_db_connection function connects to the db file specified above
    :return: connection, cursor"""
    conn = sqlite3.connect(str(DB_FILE_PATH))
    c = conn.cursor()

    return conn, c


def _initialize_db():
    """The _initialize_db function takes the schema file and creates the database
    :return: nothing"""
    conn, c = _get_db_connection()

    with open(str(SCHEMA_PATH)) as f:
        c.executescript(f.read())

    conn.close()


def _initialize_users():
    """The _initialize_users function takes the user_accounts json file and enters
    the contents into the users table
    :return: nothing"""
    if not USER_ACCOUNTS_PATH.exists():
        raise FileNotFoundError()

    with open(str(USER_ACCOUNTS_PATH)) as f:
        user_accounts = json.load(f)

    conn, c = _get_db_connection()

    c.execute('''DELETE FROM user''')

    for user in user_accounts['accounts']:
        c.execute("""INSERT INTO user VALUES (?, ?)""", (user['email'], user['password']))

    conn.commit()


def _poll_sensors(conn, cursor):
    """The _poll_sensors function inserts the data returned from the motionsensor and tempreading
    functions in catnanny.py into the sensor_data table
    :return: nothing"""
    conn, c = _get_db_connection()

    motion_reading = catnanny.motionsensor()
    temp_reading = catnanny.tempreading()

    current_timestamp = datetime.now().isoformat()
    # insert a timestamp, the word motion, and the output from catnanny.motionsensor into sensor_data
    c.execute("""INSERT INTO sensor_data VALUES (?, ?, ?)""", (current_timestamp, 'motion', motion_reading))
    # insert a timestamp, the word temperature, and the output from catnanny.tempreading into sensor_data
    c.execute("""INSERT INTO sensor_data VALUES (?, ?, ?)""", (current_timestamp, 'temperature', temp_reading))

    conn.commit()


def _clean_db(conn, cursor):
    """The _clean_db function deletes old data from the sensor_data table and leaves the last
    10000 rows
    :return: nothing"""
    conn, c =  _get_db_connection()
    # delete rows from sensor_data in descending order until 10000 are left
    c.execute("""DELETE FROM sensor_data WHERE timestamp NOT IN (SELECT timestamp FROM (SELECT timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 1 OFFSET ?) sensor)""", DB_CLEAN_MAX_RECORDS)

    conn.commit()


def main():
    # connect to the db
    conn, c = _get_db_connection()

    time_start = datetime.now()

    # wait 5 seconds then collect data from the sensors
    # remove old data from sensor_data if needed
    try:
        while True:
            time.sleep(SENSOR_POLL_DELAY)
            _poll_sensors(conn, c)
            if (datetime.now() - time_start) >= DB_CLEAN_DURATION:
                _clean_db(conn, c)
    except KeyboardInterrupt:
        conn.close()


if __name__ == '__main__':
    if not DB_FILE_PATH.exists():
        _initialize_db()

    _initialize_users()

    main()

