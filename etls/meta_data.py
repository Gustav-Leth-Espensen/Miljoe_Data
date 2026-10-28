import requests
from etls.etl import open_connection, close_connection

def extract_meta_data(limit:int, station_id:str, bbox:str = "7,54,16,58", status = "Active"):
    url = "https://opendataapi.dmi.dk/v2/metObs/collections/station/items"
    url += f"?bbox={bbox}" + f"&status={status}" #### DET ER VIGTIGT DER IKKE ER ET '&' FØR LIMIT
    if limit:
        url += f"&limit={limit}"
    if station_id:
        url += f"&stationId={station_id}"


    response = requests.get(url)
    if not response.ok:  ### Returns false if response error is 400+
        raise ValueError("Input in extract outside of API scope.")
    extracted_metadata = response.json()
    return extracted_metadata


def transform_meta_data(extracted_metadata):
    try:
        data = extracted_metadata['features']
    except KeyError:
        raise KeyError(
            "Missing key in data.")
    transformed_data = {}
    list_stations_id_name_coordinates = []
    for raw_data in data:
        data_prop=raw_data["properties"]
        name = data_prop['name']
        station_id = data_prop['stationId']

        data_geo = raw_data['geometry']
        coordinates_long = data_geo['coordinates'][0]   #longitude in WGS84
        coordinates_lat = data_geo['coordinates'][1]  # latitude in WGS84

        if not name or not station_id or (not coordinates_long and coordinates_long != 0) or (not coordinates_lat and coordinates_lat != 0):
            raise ValueError("One of parameters not found.")
        #
        if station_id not in transformed_data:
            transformed_data[station_id] = [name]
            list_stations_id_name_coordinates.append([station_id, name, coordinates_long, coordinates_lat])

    return list_stations_id_name_coordinates



def load_meta_data(list_stations_id_name_coordinates):
    conn = open_connection()
    cursor = conn.cursor()
    insert_query = """
                   INSERT INTO meta_data(station_id, name, coordinates_longitude, coordinates_latitude)
                   VALUES(%s, %s, %s, %s);
                   """

    cursor.executemany(insert_query,list_stations_id_name_coordinates)
    conn.commit()
    close_connection(cursor,conn)
    return

