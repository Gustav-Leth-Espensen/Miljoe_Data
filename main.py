import psycopg
import etl

if __name__ == '__main__':
    extracted_data = etl.extract_from_dmi()
    transformed_data = etl.transform(extracted_data)
    etl.load_humidity(transformed_data)
    etl.load_temp_dry(transformed_data)
    etl.load_pressure(transformed_data)


