import requests
import psycopg
import os

### datetime; is the start and end dates with timezone
### in this format: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
### limit; set number of observation up to 300.000
### offset; makes observations start from that number, needs to be less than total observations left in dataset
### bbox; is area measured, standard set to Denmark
def extract_from_dmi(datetime:str, limit:int, offset:int, bbox:str = "7,54,16,58", all_data:bool = True, parameter_id:str = "temp_dry"):
    url = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"
    if all_data:
        dmi_parameters = {
            "datetime": datetime,
            "limit": limit,
            "offset": offset,
            "bbox": bbox
        }
    else:
        dmi_parameters = {
            "datetime": datetime,
            "limit": limit,
            "offset": offset,
            "bbox": bbox,
            "parameterId": parameter_id
        }

    response = requests.get(url, params=dmi_parameters)
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
            "Called data from wrong API, try looking at https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api")

    # if "features" not in extracted_data.keys(): ###Tjekke for mere (geometri)
    #     raise AttributeError("Called data from wrong API, try looking at \n https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api")
    # data = extracted_data['features']
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
                   INSERT INTO temp_dry(station_id, observed_time, temperature)
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
                   INSERT INTO humidity(station_id, observed_time, percent_humidity)
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
                   INSERT INTO pressure(station_id, observed_time, mbar)
                   VALUES (%s, %s, %s);
                   """

    cursor.executemany(insert_query, data)
    conn.commit()
    close_connection(cursor, conn)
    return


#### NOT IN USE RIGHT NOW (DONT LOOK RASMUS)
### Det er farligt at skrive {key} ind i string da folk kan give en key som er database down
### Tag nogle enkelt og hardcode det
### Denne function tager alle forskellige keys og sætter data ind hvis tabellen existere
# def load(transformed_data):
#     keys_list = list(transformed_data.keys())
#     for key in keys_list:
#         for i in range(len(transformed_data[key])):
#             station_id = transformed_data[key][i][0]
#             date_and_time = transformed_data[key][i][1]
#             value = transformed_data[key][i][2]
#             cursor.execute(
#             f"INSERT INTO {key}(station_id, date_time, value_d) VALUES(%s, %s, %s)",
#             (station_id, date_and_time, value)
#             )
#     return



#### NOT IN USE RIGHT NOW (DONT LOOK RASMUS)
#### TRANFORMS DATA INTO DICT IN DICT IN DICT
# def transform1():
#     temp_datetime = "2018-02-12T01:00:00Z/2018-02-12T01:00:00Z"
#     data = extract_from_dmi(temp_datetime,10,0)
#     outer_dict = {}
#
#     for i in range(len(data['features'])):
#         date_and_time = data['features'][i]['properties']['observed'][:-1]
#         first_dict_layer = data['features'][i]['properties']['parameterId']
#         second_dict_layer = data['features'][i]['properties']['stationId']
#         if data['features'][i]['properties']['parameterId'] not in outer_dict.keys():
#             first_dict_layer = data['features'][i]['properties']['parameterId']
#             outer_dict[first_dict_layer] = {}
#             if data['features'][i]['properties']['stationId'] not in outer_dict[first_dict_layer].keys():
#                 second_dict_layer = data['features'][i]['properties']['stationId']
#                 outer_dict[first_dict_layer][second_dict_layer] = {}
#                 outer_dict[first_dict_layer][second_dict_layer][date_and_time] = data['features'][i]['properties'][
#                     'value']
#             else:
#                 outer_dict[first_dict_layer][second_dict_layer][date_and_time] = data['features'][i]['properties'][
#                     'value']
#         elif data['features'][i]['properties']['stationId'] not in outer_dict[first_dict_layer].keys():
#             second_dict_layer = data['features'][i]['properties']['stationId']
#             outer_dict[first_dict_layer][second_dict_layer] = {}
#             outer_dict[first_dict_layer][second_dict_layer][date_and_time] = data['features'][i]['properties']['value']
#         else:
#             outer_dict[first_dict_layer][second_dict_layer][date_and_time] = data['features'][i]['properties']['value']
#     return outer_dict
