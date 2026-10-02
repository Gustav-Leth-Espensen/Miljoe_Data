import psycopg2

conn = psycopg2.connect(
dbname="test_1234",
user="postgres",
password="Agurk_1234",
host="localhost",
port=5432
)

cursor = conn.cursor()

# cursor.execute("SELECT * FROM dmi_data;")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

cursor.execute(
"INSERT INTO dmi_data(observation, stations_id, obs_time, obs_value) VALUES(%s, %s, %s, %s)",
("regn igen", "70770", "2300-2400", 25)
)
conn.commit()

cursor.close()
conn.close()