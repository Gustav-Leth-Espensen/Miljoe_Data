import etls.etl as etl
import etls.meta_data as meta

if __name__ == '__main__':
    meta_data = meta.extract_meta_data(limit = 2000, station_id="")
    meta_list = meta.transform_meta_data(meta_data)
    meta.load_meta_data(meta_list)

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


