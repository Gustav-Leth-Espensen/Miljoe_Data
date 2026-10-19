import etl
import stationID_to_database as Sta

if __name__ == '__main__':
    meta_data = Sta.extract_meta_data()
    meta_list = Sta.transform_meta_data(meta_data)
    Sta.load_meta_data(meta_list)

    extracted_data = etl.extract_from_dmi("2018-02-12T01:00:00Z/2018-02-12T01:00:00Z", 100, 0)
    transformed_data = etl.transform(extracted_data)
    etl.load_humidity(transformed_data)
    etl.load_temp_dry(transformed_data)
    etl.load_pressure(transformed_data)


