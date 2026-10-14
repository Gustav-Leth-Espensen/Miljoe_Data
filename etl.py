import requests
import psycopg

### datetime; is the start and end dates with timezone
### in this format: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
### limit; set number of observation up to 300.000
### offset; makes observations start from that number, needs to be less than total observations left in dataset
### bbox; is area measured, standard set to Denmark
def extract_from_dmi(datetime:str, limit:int, offset:int, bbox:str = "7,54,16,58"):
    url = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"
    dmi_parameters = {
        "datetime": datetime,
        "limit": limit,
        "offset": offset,
        "bbox": bbox
    }

    response = requests.get(url, params=dmi_parameters)
    if not response.ok:  ### Returns false if response error is 400+
        return "Failed API response"
    extracted_data = response.json()
    return extracted_data

#temp_datetime = "2018-02-12T01:00:00Z/2018-02-12T01:00:00Z"
#print(extract_from_dmi(temp_datetime,2,0))

#tilføj tjek for om indhentet data er korrekt
def transform(extracted_data):
    if extracted_data == {}:
        return "This is an empty dictionary"

    if extracted_data == "Failed API response":
        return "Failed API response"

    if "features" not in extracted_data.keys():
        return "Called data from wrong API, try looking at \n https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api"
    #keys=extracted_data.keys()
    #if "FeatureCollection" !=keys[0] and "feature"!=keys[1] and "timeStamp"!=keys[2] and "numberReturned"!=keys[3] and "links" !=keys[4]:
        #return "Called data from wrong API, try looking at \n https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api"
    
    data = extracted_data['features'] ### Det er lidt underligt at ændre navnet her, skal vi gøre det i toppen eller lade helt være?
    transformed_data={}
    missing_parameter_id_count = 0
    missing_value_count = 0
    for i in data:
        datain=i["properties"]
        parameter_id = datain['parameterId']
        station_id = datain['stationId']
        date_and_time =datain['observed']
        value =datain['value']

        if not parameter_id: ### skal vi tjekke for NaN
            missing_parameter_id_count =+ 1
            continue
        if not value and value != 0.0: ### skal vi tjekke for NaN
            missing_value_count =+ 1
            continue
        if not station_id: 
            print("Parameter has no station_id, data entry still saved.")#snak med Rasmus
        if not date_and_time:
            print("Parameter has no station_id or date/time, data entry still saved.")
        if not date_and_time: #snak med Rasmus
            print("Parameter has no date/time, data entry still saved.")

        if parameter_id not in transformed_data.keys():
            transformed_data[parameter_id] = []
            transformed_data[parameter_id].append([station_id, date_and_time, value])
        else:
            transformed_data[parameter_id].append([station_id, date_and_time, value])

    print(f"Missing parameter ID in {missing_parameter_id_count} observations")
    print(f"Missing value in {missing_value_count} observations")
    return transformed_data

def open_connection():
    conn = psycopg.connect(
        "postgresql://app:test@db:5432/data_db"
    )
    return conn

def close_connection(cursor,conn):
    cursor.close()
    conn.close()


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


#
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

def etl(datetime:str, limit:int, offset:int, bbox:str = "7,54,16,58"):
    raw_data = extract_from_dmi(datetime, limit, offset, bbox)
    trans_data = transform(raw_data)
    load_humidity(trans_data)
    load_pressure(trans_data)
    load_temp_dry(trans_data)
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
# def transform(extracted_data):
#     data = extract_from_dmi()
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
