import psycopg


##### Laves om til string ting
## host er db når appen er indeni docker
# conn = psycopg.connect(
# conn_string = "postgresql://app:test@db:5432/data_db"
# )

# conn = psycopg.connect(
# "postgresql://app:test@localhost:5432/data_db"
# )


def create_table_sql():
    create_table = """
    CREATE TABLE IF NOT EXISTS test (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
    )
    """
    return create_table


# cursor = conn.cursor()

# cursor.execute("SELECT * FROM test;")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# cursor.execute(
# "INSERT INTO test(product_id, name, price) VALUES(%s, %s, %s)",
# (1, "test", 25.2)
# )
#
# conn.commit()
# cursor.close()
# conn.close()