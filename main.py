import psycopg
import etl

if __name__ == '__main__':
    extracted_data = etl.extract_from_dmi()
    transformed_data = etl.transform(extracted_data)
    humid = etl.transform(extracted_data)['humidity']
    etl.load_humidity(humid)
