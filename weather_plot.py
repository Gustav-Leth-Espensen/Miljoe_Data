import numpy as np
import matplotlib.pyplot as plt
import psycopg
import dotenvx
import os


def open_connection():
    dotenvx.load_dotenv()
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

# a = extract_meta_data_from_db("06019")
# print(a)

def sort_data_after_date(data_from_own_database):
    sortorder = np.argsort(data_from_own_database[:,2])
    sorted_data = data_from_own_database[sortorder]
    return sorted_data

def create_plot_one_station(parameter_id ,station_id, marker):
    if parameter_id == "temp_dry":
        station_data = extract_temp_dry_from_db(station_id)
    elif parameter_id == "humidity":
        station_data = extract_humidity_from_db(station_id)
    elif parameter_id == "pressure":
        station_data = extract_pressure_from_db(station_id)
    else:
        return "Please choose valid parameter ID"
    sorted_station_data = sort_data_after_date(station_data)
    label_station_name = extract_meta_data_from_db(station_id)[0,1]
    plt.plot(sorted_station_data[:, 2], sorted_station_data[:, 3], marker, label = label_station_name)
    return f"Plot for {parameter_id} at station {station_id} ready."

# create_plot_one_station("humidity","06019", 'r.')
# create_plot_one_station("humidity","06030", 'b.')
# plt.legend()
# plt.title("Humidity")
# plt.show()

# a = extract_humidity_from_db("06019")
a = extract_temp_dry_from_db("06019")
# print(a[:,3])

plt.hist(a[:,3], bins = 50)
plt.show()

