import psycopg
import etl

if __name__ == '__main__':
    extracted_data = etl.extract_from_dmi("2018-02-12T01:00:00Z/2018-02-12T01:00:00Z", 100, 0)
    transformed_data = etl.transform(extracted_data)
    etl.load_humidity(transformed_data)
    etl.load_temp_dry(transformed_data)
    etl.load_pressure(transformed_data)


