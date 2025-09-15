import psycopg2
import traceback

try:
    conn = psycopg2.connect(
        dbname="mydb",
        user="myuser",
        password="mypass",
        host="127.0.0.1",
        port="5433"
    )
    print("✅ 연결 성공!")
    conn.close()
except Exception as e:
    print("❌ 연결 실패")
    traceback.print_exc()
