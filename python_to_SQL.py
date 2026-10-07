import psycopg

conn = psycopg.connect(
dbname="test_1234",
user="postgres",
password="Agurk_1234",
host="localhost",
port=5432
)



##### Laves om til string ting
### host er db
# conn = psycopg.connect(
# conn_string = "postgresql://app:test@db:5432/miljoe_data"
# )
#
# def create_table_sql():
#     create_table = """
#     CREATE TABLE IF NOT EXISTS test (
#     product_id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     price FLOAT NOT NULL
#     )
#     """
#     return create_table


cursor = conn.cursor()

# cursor.execute("SELECT * FROM dmi_data;")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute(
# "INSERT INTO dmi_data(observation, stations_id, obs_time, obs_value) VALUES(%s, %s, %s, %s)",
# ("regn igen", "70770", "2300-2400", 25)
# )
conn.commit()

cursor.close()
conn.close()