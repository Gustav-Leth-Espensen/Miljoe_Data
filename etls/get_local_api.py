import requests
import os
import dotenvx
import json

def extract_data_from_local_api():
    dotenvx.load_dotenv()
    url = "https://herodot.spac.dk/api/v1/observations"
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

# data = extract_data_from_local_api()

# with open('data.json', 'w') as file:
#     json.dump(data, file)

def node_translater(json_data):
    #### FIND UD AF HVILKEN DER ER RIGTIG:
    #### json_data['observations']['nodeId']
    ballerup_sensor ="6d437168-7432-470b-9cf4-08439d0127ad"
    odsense_sensor = "ae6901bb-6703-4955-9d59-179c1ee5dae8"
    aarhus_sensor = "2c47284d-777b-44f0-bdeb-3d442f6a31b1"
    return

def transform_local_data(json_data):
    transformed_local_data = []
    data_dict = json_data['observations']

    for observation in data_dict:
        instrument_model = observation['instrumentModel']
        parameter_id = observation['sensor']
        timestamp = observation['timestamp']
        value = observation['value']

        # if not parameter_id or not instrument_model or not timestamp or (not value and value != 0):
            # raise ValueError("One of parameters not found.")

        transformed_local_data.append([instrument_model, parameter_id, timestamp, value])

    return transformed_local_data

data = extract_data_from_local_api()
transformed_data = transform_local_data(data)
print(transformed_data)


#### FUCK MED EGEN API AT