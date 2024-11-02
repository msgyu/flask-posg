from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="test_db",
        user="postgres",
        password="password"
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # テーブルが存在しない場合は作成
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    # サンプルデータがなければ挿入
    cur.execute("SELECT COUNT(*) FROM messages")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO messages (content) VALUES (%s)", ("Hello from the database!",))
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def hello_world():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT content FROM messages LIMIT 1")
    message = cur.fetchone()[0]
    cur.close()
    conn.close()
    return message

if __name__ == "__main__":
    init_db()  # アプリ起動時に初期化を実行
    app.run(host="0.0.0.0", port=5000)

