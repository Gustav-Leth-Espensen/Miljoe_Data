import requests
import psycopg

def extract_from_dmi():
    url = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"

    dmi_parameters = {
        "datetime": "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z",
        "limit": "1000",
        "offset": "0",
        "bbox": "7,54,16,58"
    }
    response = requests.get(url, params=dmi_parameters)
    extracted_data = response.json()
    return extracted_data

# print(extract_from_dmi())
#tilføj tjek for om indhentet data er korrekt
def transform(extracted_data):
    data = extracted_data
    outer_dict = {}
    for i in range(len(data['features'])):
        parameter_id = data['features'][i]['properties']['parameterId']
        station_id = data['features'][i]['properties']['stationId']
        date_and_time = data['features'][i]['properties']['observed'][:-1]
        value = data['features'][i]['properties']['value']
        if data['features'][i]['properties']['parameterId'] not in outer_dict.keys():
            outer_dict[parameter_id] = []
            outer_dict[parameter_id].append([station_id, date_and_time, value])
        else:
            outer_dict[parameter_id].append([station_id, date_and_time, value])

    return outer_dict

# print(transform(extract_from_dmi()))
# humid = transform(extract_from_dmi())['humidity']

conn = psycopg.connect(
    "postgresql://app:test@db:5432/data_db"
)
cursor = conn.cursor()

def load_humidity(transformed_data):
    for i in range(len(transformed_data)):
        cursor.execute(
        "INSERT INTO humidity(station_id, date_time, value_d) VALUES(%s, %s, %s)",
        (transformed_data[i][0], transformed_data[i][1], transformed_data[i][2])
        )

    conn.commit()
    cursor.close()
    conn.close()






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
