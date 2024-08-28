# Flask application with endpoints for data retrieval and data addition.
# app.py
from flask import Flask, request, jsonify
import redis
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

# Redis connection setup
r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0)

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
