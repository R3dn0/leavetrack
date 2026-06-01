from config.database import get_connection

if __name__ == "__main__":
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT first_name, last_name FROM employee")
                rows = cur.fetchall()

                for row in rows:
                    print(f"- {row[0]} {row[1]}")

    except Exception as e:
        print(f"Connection error : {e}")