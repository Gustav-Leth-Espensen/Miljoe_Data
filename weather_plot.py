import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats
import requests


def extract_weather_data_from_own_db(parameter_id:str, station_id:str, start_data:str, end_date:str, limit: int = 100):
    url = "http://127.0.0.1:8000/" + parameter_id + "?"
    url +=f"limit={limit}" #### DET ER VIGTIGT DER IKKE ER ET '&' FØR LIMIT
    if station_id:
        url +=f"&station_id={station_id}"
    if start_data:
        url +=f"&start_date={start_data}"
    if end_date:
        url +=f"&end_date={end_date}"

    response = requests.get(url)
    if not response.ok:  ### Returns false if response error is 400+
        raise ValueError("Input in extract outside of API scope.")
    extracted_data = response.json()
    return extracted_data

# print(extract_weather_data_from_own_db("humidity", station_id="", start_data="", end_date=""))


def extract_meta_data_from_own_api():
    url = "http://127.0.0.1:8000/stations"
    response = requests.get(url)
    if not response.ok:  ### Returns false if response error is 400+
        raise ValueError("Input in extract outside of API scope.")
    meta_data = response.json()
    return meta_data

# print(extract_meta_data_from_own_api())

def transform_data_from_own_db(extracted_data, measurement_type):
    id_list = []
    station_id_list = []
    observed_time_list = []
    value_list = []

    for raw_data in extracted_data:
        id_obs = raw_data['id']
        station_id = raw_data['station_id']
        observed_time = raw_data['observed_time']
        value = raw_data[measurement_type]

        id_list.append(id_obs)
        station_id_list.append(station_id)
        observed_time_list.append(observed_time)
        value_list.append(value)

    id_list = np.asarray(id_list, dtype=int)
    station_id_list = np.asarray(station_id_list, dtype=str)
    observed_time_list = np.asarray(observed_time_list, dtype=np.datetime64)
    value_list = np.asarray(value_list, dtype=float)

    return id_list, station_id_list, observed_time_list, value_list

def transform_meta_data_from_own_api(meta_data):
    id_list = []
    station_id_list = []
    name_list = []
    coordinates_longitude_list = []
    coordinates_latitude_list = []

    for raw_data in meta_data:
        id_obs = raw_data['id']
        station_id = raw_data['station_id']
        name = raw_data['name']
        coordinates_longitude = raw_data['coordinates_longitude']
        coordinates_latitude = raw_data['coordinates_latitude']

        id_list.append(id_obs)
        station_id_list.append(station_id)
        name_list.append(name)
        coordinates_longitude_list.append(coordinates_longitude)
        coordinates_latitude_list.append(coordinates_latitude)

    id_list = np.asarray(id_list, dtype=int)
    station_id_list = np.asarray(station_id_list, dtype=str)
    name_list = np.asarray(name_list, dtype=str)
    coordinates_longitude_list = np.asarray(coordinates_longitude_list, dtype=float)
    coordinates_latitude_list = np.asarray(coordinates_latitude_list, dtype=float)

    return id_list, station_id_list, name_list, coordinates_longitude_list, coordinates_latitude_list

# raw_humidity_data =extract_weather_data_from_own_db("humidity", station_id="06019", start_data="", end_date="", limit=500)
# humidity_data = transform_data_from_own_db(raw_humidity_data, "percent_humidity")
# print(humidity_data[0])

# raw_meta_data = extract_meta_data_from_own_api()
# test_meta_data = transform_meta_data_from_own_api(raw_meta_data)
# print(test_meta_data[2][test_meta_data[1] == "06019"])


def sort_data_after_datetime(data_from_own_database):
    sortorder = np.argsort(data_from_own_database[2])
    sorted_id_list = data_from_own_database[0][sortorder]
    sorted_station_id_list = data_from_own_database[1][sortorder]
    sorted_observed_time_list = data_from_own_database[2][sortorder]
    sorted_value_list = data_from_own_database[3][sortorder]
    return sorted_id_list, sorted_station_id_list, sorted_observed_time_list, sorted_value_list


# raw_humidity_data =extract_weather_data_from_own_db("temperature", station_id="06019", start_data="", end_date="", limit=1000)
# humidity_data = transform_data_from_own_db(raw_humidity_data, "temperature")
# print(sort_data_after_datetime(humidity_data)[3].dtype)

##### NEEDS STATION ID AND START/END DATE
def create_plot_one_station(parameter_id ,station_id, measurement_type ,marker):
    data_extracted_from_own_api = extract_weather_data_from_own_db(parameter_id=parameter_id, station_id=station_id,start_data="", end_date="", limit=1000)
    station_data = transform_data_from_own_db(data_extracted_from_own_api, measurement_type)
    sorted_station_data = sort_data_after_datetime(station_data)

    raw_meta_data = extract_meta_data_from_own_api()
    meta_data = transform_meta_data_from_own_api(raw_meta_data)

    label_station_name = meta_data[2][meta_data[1] == station_id]

    plt.plot(sorted_station_data[2], sorted_station_data[3], marker, label = label_station_name)
    return f"Plot for {parameter_id} at station {station_id} ready."

create_plot_one_station("temperature","06019", "temperature", 'r.')
create_plot_one_station("temperature","06030", "temperature", 'b.')
plt.legend()
# plt.title("Humidity")
plt.show()




