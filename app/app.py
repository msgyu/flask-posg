from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)

# データベース接続関数
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

# 初回起動時にテーブル作成とサンプルデータの挿入を行う
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    cur.execute("SELECT COUNT(*) FROM messages")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO messages (content) VALUES (%s)", ("Hello from the database!",))
    conn.commit()
    cur.close()
    conn.close()

# ルートエンドポイント
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
