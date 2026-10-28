import requests
import psycopg
import os

### datetime; is the start and end dates with timezone
### in this format: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
### limit; set number of observation up to 300.000
### offset; makes observations start from that number, needs to be less than total observations left in dataset
### bbox; is area measured, standard set to Denmark
def extract_weather_data_from_dmi(datetime:str, limit:int, offset:int, parameter_id:str, bbox:str = "7,54,16,58"):
    url = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"
    url += f"?bbox={bbox}" #### DET ER VIGTIGT DER IKKE ER ET '&' FØR LIMIT
    if datetime:
        url += f"&datetime={datetime}"
    if limit:
        url += f"&limit={limit}"
    if offset:
        url += f"&offset={offset}"
    if parameter_id:
        url += f"&parameterId={parameter_id}"


    response = requests.get(url)
    if not response.ok:  ### Returns false if response error is 400+
        raise ValueError("Input in extract outside of API scope.")
    extracted_data = response.json()
    return extracted_data


# temp_datetime = "2018-02-12T01:00:00Z/2018-02-12T01:00:00Z"
# extract_from_dmi(temp_datetime,10,0)


def transform(extracted_data):
    if extracted_data == {}:
        raise ValueError("Trying to transform an empty dictionary.")

    try:
        data = extracted_data['features']
    except KeyError:
        raise KeyError(
            "Missing key in data.")

    transformed_data = {}

    for raw_data in data:
        data_prop=raw_data["properties"]
        parameter_id = data_prop['parameterId']
        station_id = data_prop['stationId']
        date_and_time =data_prop['observed']
        value =data_prop['value']

        if not parameter_id or not station_id or not date_and_time or (not value and value != 0):
            raise ValueError("One of parameters not found.")

        if parameter_id not in transformed_data.keys():
            transformed_data[parameter_id] = []
            transformed_data[parameter_id].append([station_id, date_and_time, value])
        else:
            transformed_data[parameter_id].append([station_id, date_and_time, value])

    return transformed_data

# temp_datetime = "2018-02-12T01:00:00Z/2018-02-12T01:00:00Z"
# print(transform(extract_from_dmi(temp_datetime,10,0)))

# print(transform(extract_from_dmi(temp_datetime,2,0 )))
# print(list(transform(extract_from_dmi()).keys()))

def open_connection():
    url = str(os.getenv('DATABASE_URL'))
    conn = psycopg.connect(
        url
    )
    return conn

def close_connection(cursor,conn):
    cursor.close()
    conn.close()


def load_temp_dry(transformed_data):
    conn = open_connection()
    cursor = conn.cursor()
    data = transformed_data['temp_dry']
    insert_query = """
                   INSERT INTO dmi_temp_dry(station_id, observed_time, celsius)
                   VALUES (%s, %s, %s);
                   """

    cursor.executemany(insert_query, data)
    conn.commit()
    close_connection(cursor, conn)
    return


def load_humidity(transformed_data):
    conn = open_connection()
    cursor = conn.cursor()
    data = transformed_data['humidity']
    insert_query = """
                   INSERT INTO dmi_humidity(station_id, observed_time, percent_humidity)
                   VALUES(%s, %s, %s);
                   """

    cursor.executemany(insert_query,data)
    conn.commit()
    close_connection(cursor,conn)
    return


def load_pressure(transformed_data):
    conn = open_connection()
    cursor = conn.cursor()
    data = transformed_data['pressure']
    insert_query = """
                   INSERT INTO dmi_pressure(station_id, observed_time, hPa)
                   VALUES (%s, %s, %s);
                   """

    cursor.executemany(insert_query, data)
    conn.commit()
    close_connection(cursor, conn)
    return
