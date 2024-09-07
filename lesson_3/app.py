# Flask application with endpoints for data retrieval and data addition.
# app.py
from flask import Flask, request, jsonify
import redis
import psycopg2
import os

app = Flask(__name__)

# Print environment variables for debugging
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_NAME:", os.getenv('DB_NAME'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("REDIS_HOST:", os.getenv('REDIS_HOST'))
print("REDIS_PORT:", os.getenv('REDIS_PORT'))

# PostgreSQL connection setup
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        raise

# Redis connection setup
try:
    r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0)
except Exception as e:
    print("Error connecting to Redis:", e)
    raise

# Ensure usersTbl table exists
def ensure_table_exists():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usersTbl (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

ensure_table_exists()

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usersTbl;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/data', methods=['POST'])
def add_data():
    conn = get_db_connection()
    cur = conn.cursor()
    content = request.json
    cur.execute("INSERT INTO usersTbl (id, name) VALUES (%s, %s)", 
                (content['id'], content['name']))
    conn.commit()
    cur.close()
    conn.close()
    r.set(content['id'], content['name'])
    return 'Data added', 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
