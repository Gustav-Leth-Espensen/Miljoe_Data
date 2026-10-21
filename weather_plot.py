import numpy as np
import matplotlib.pyplot as plt
import psycopg
import dotenv
import os
import datetime


def open_connection():
    dotenv.load_dotenv()
    url = str(os.getenv('LOCAL_URL'))
    conn = psycopg.connect(
        url
    )
    return conn

def close_connection(cursor,conn):
    cursor.close()
    conn.close()

def extract_meta_data_from_db(station_id):
    conn = open_connection()
    cursor = conn.cursor()
    data_query = """
                 SELECT id, name, station_id, coordinates_longitude, coordinates_latitude FROM meta_data WHERE station_id = %s
                 """
    cursor.execute(data_query, (station_id,))
    data = cursor.fetchall()
    close_connection(cursor, conn)
    data = np.asarray(data)
    return data

def extract_temp_dry_from_db(station_id):
    conn = open_connection()
    cursor = conn.cursor()
    data_query = """
                 SELECT id, station_id, observed_time, temperature FROM temp_dry WHERE station_id = %s
                 """
    cursor.execute(data_query, (station_id,))
    data = cursor.fetchall()
    close_connection(cursor, conn)
    data = np.asarray(data)
    return data

def extract_humidity_from_db(station_id):
    conn = open_connection()
    cursor = conn.cursor()
    data_query = """
                 SELECT id, station_id, observed_time, percent_humidity FROM humidity WHERE station_id = %s
                 """
    cursor.execute(data_query, (station_id,))
    data = cursor.fetchall()
    close_connection(cursor, conn)
    data = np.asarray(data)
    return data

def extract_pressure_from_db(station_id):
    conn = open_connection()
    cursor = conn.cursor()
    data_query = """
                 SELECT id, station_id, observed_time, mbar FROM pressure WHERE station_id = %s
                 """
    cursor.execute(data_query, (station_id,))
    data = cursor.fetchall()
    close_connection(cursor, conn)
    data = np.asarray(data)
    return data

a = extract_meta_data_from_db("06019")
print(a)

# b = extract_humidity_from_db("06019")
# print(b)

# c = extract_pressure_from_db("06030")
# print(c)

# d = extract_temp_dry_from_db("06019")
# print(d)

