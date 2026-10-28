import etls.etl as etl
import etls.meta_data as meta
import etls.get_local_api as lapi
import json


if __name__ == '__main__':
    meta_data = meta.extract_meta_data(limit = 2000, station_id="")
    meta_list = meta.transform_meta_data(meta_data)
    for i in lapi.meta_data_local_api():
        meta_list.append(i)
    meta.load_meta_data(meta_list)

    # with open('meta_data.json', 'w') as f:
    #     json.dump(meta_data, f)

    date_time = "2018-02-12T01:00:00Z/2018-03-15T01:00:00Z"
    extracted_data_temp_dry = etl.extract_weather_data_from_dmi(date_time, 10000, 0, "temp_dry")
    transformed_data_temp_try = etl.transform(extracted_data_temp_dry)
    etl.load_temp_dry(transformed_data_temp_try)

    extracted_data_humidity = etl.extract_weather_data_from_dmi(date_time, 10000, 0, "humidity")
    transformed_data_humidity = etl.transform(extracted_data_humidity)
    etl.load_humidity(transformed_data_humidity)

    extracted_data_pressure = etl.extract_weather_data_from_dmi(date_time, 10000, 0, "pressure")
    transformed_data_pressure = etl.transform(extracted_data_pressure)
    etl.load_pressure(transformed_data_pressure)

    local_data = lapi.extract_data_from_local_api()
    transformed_local_data = lapi.transform_local_data(local_data)
    lapi.load_local_temperature_data(transformed_local_data[0])
    lapi.load_local_humidity_data(transformed_local_data[1])
    lapi.load_local_pressure_data(transformed_local_data[2])
    lapi.load_local_co2_data(transformed_local_data[3])


