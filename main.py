import psycopg
import python_to_SQL as p2s

if __name__ == '__main__':
    print("Hello World")

    conn = psycopg.connect(
    "postgresql://app:test@db:5432/data_db"
    )
    cursor = conn.cursor()

    cursor.execute(p2s.create_table_sql())
    conn.commit()
    cursor.close()
    conn.close()