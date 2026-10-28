import requests
import os
import etls.etl as etl

def extract_data_from_local_api():
    url = "https://herodot.spac.dk/api/v1/observations?limit=5000"
    aut_value = str(os.getenv('API_TOKEN'))

    request_header = {
        'Authorization': f'Bearer {aut_value}'
    }

    response = requests.get(url, headers = request_header)
    # print(response.status_code)
    if not response.ok:  ### Returns false if response error is 400+
        raise ValueError("Input in extract outside of API scope.")
    extracted_data = response.json()
    return extracted_data


def node_translater(node_id):
    if node_id == "ae6901bb-6703-4955-9d59-179c1ee5dae8":
        return "BAL01"
    elif node_id == "2c47284d-777b-44f0-bdeb-3d442f6a31b1":
        return "ODE01"
    elif node_id == "6d437168-7432-470b-9cf4-08439d0127ad":
        return "AAR01"
    elif node_id == "33616cde-3d37-41fc-b698-f6e2e5640236":
        return "BAL02"
    else:
        raise ValueError("Node_id does not exist")

def meta_data_local_api():
    local_meta_data_list = []
    ballerup_meta = ["BAL01", "Specialisterne Ballerup", 10.21076, 56.15674]
    odense_meta = ["ODE01", "Specialisterne Odense", 10.38831, 55.39594]
    aarhus_meta = ["AAR01", "Specialisterne Aarhus", 12.36328, 55.73165]
    ballerup_meta_2 = ["BAL02", "Specialisterne Ballerup", 10.21076, 56.15674]
    local_meta_data_list.append(ballerup_meta)
    local_meta_data_list.append(odense_meta)
    local_meta_data_list.append(aarhus_meta)
    local_meta_data_list.append(ballerup_meta_2)
    return local_meta_data_list


def transform_local_data(json_data):
    transformed_local_temp_data = []
    transformed_local_humidity_data = []
    transformed_local_pressure_data = []
    transformed_local_co2_data = []
    data_dict = json_data['observations']

    ##### observations ID er unikt

    for observation in data_dict:
        instrument_model = observation['instrumentModel']
        parameter_id = observation['sensor']
        timestamp = observation['timestamp']
        value = observation['value']
        station_id = observation['nodeId']
        personalized_id = node_translater(station_id)
        observation_id = observation['observationId']

        if parameter_id == "temperature" or (parameter_id == "" and instrument_model == "DS18B20"):
            transformed_local_temp_data.append([observation_id, instrument_model, personalized_id, timestamp, value])
        elif parameter_id == "humidity":
            transformed_local_humidity_data.append([observation_id, instrument_model, personalized_id, timestamp, value])
        elif parameter_id == "pressure":
            transformed_local_pressure_data.append([observation_id, instrument_model, personalized_id, timestamp, value])
        elif parameter_id == "co2_concentration":
            transformed_local_co2_data.append([observation_id, instrument_model, personalized_id, timestamp, value])
        else:
            raise KeyError("Error in data from local API")


    return transformed_local_temp_data, transformed_local_humidity_data, transformed_local_pressure_data, transformed_local_co2_data

def load_local_meta_data():
    return

# data = extract_data_from_local_api()
# transformed_data = transform_local_data(data)
# print(transformed_data[3])

def load_local_temperature_data(transformed_local_data_temp):
    conn = etl.open_connection()
    cursor = conn.cursor()
    insert_query = """
                   INSERT INTO local_temperature(observation_id,instrument_model, station_id, observed_time, celsius)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (observation_id) DO NOTHING;
                   """

    cursor.executemany(insert_query, transformed_local_data_temp)
    conn.commit()
    etl.close_connection(cursor, conn)
    return

def load_local_humidity_data(transformed_local_data_humidity):
    conn = etl.open_connection()
    cursor = conn.cursor()
    insert_query = """
                   INSERT INTO local_humidity(observation_id, instrument_model, station_id, observed_time, percent_humidity)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (observation_id) DO NOTHING;
                   """

    cursor.executemany(insert_query, transformed_local_data_humidity)
    conn.commit()
    etl.close_connection(cursor, conn)
    return

def load_local_pressure_data(transformed_local_data_pressure):
    conn = etl.open_connection()
    cursor = conn.cursor()
    insert_query = """
                   INSERT INTO local_pressure(observation_id, instrument_model, station_id, observed_time, pascal)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (observation_id) DO NOTHING;
                   """

    cursor.executemany(insert_query, transformed_local_data_pressure)
    conn.commit()
    etl.close_connection(cursor, conn)
    return

def load_local_co2_data(transformed_local_data_co2):
    conn = etl.open_connection()
    cursor = conn.cursor()
    insert_query = """
                   INSERT INTO local_CO2(observation_id, instrument_model, station_id, observed_time, ppm)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (observation_id) DO NOTHING;
                   """

    cursor.executemany(insert_query, transformed_local_data_co2)
    conn.commit()
    etl.close_connection(cursor, conn)
    return

#### VI LEGEDE MED EGEN SENSOR 28.10.2026 08:30:00 ->