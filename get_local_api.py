import requests
import os
import dotenvx

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

# print(extract_data_from_local_api())