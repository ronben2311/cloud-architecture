# Flask application with endpoints for data retrieval and data addition.
# app.py
from flask import Flask, request, jsonify
import redis
import psycopg2

app = Flask(__name__)

# PostgreSQL connection setup
conn = psycopg2.connect(
    dbname="lessonFourDB",
    user="lessonFourUser",
    password="lessonFourPassword",
    host="yourdbhost"
)
cur = conn.cursor()

# Redis connection setup
r = redis.Redis(host='yourredisservice', port=6379, db=0)

@app.route('/data', methods=['GET'])
def get_data():
    cur.execute("SELECT * FROM mainTable;")
    data = cur.fetchall()
    return jsonify(data)

@app.route('/data', methods=['POST'])
def add_data():
    content = request.json
    cur.execute("INSERT INTO mainTable (id, name) VALUES (%s, %s)", 
                (content['id'], content['name']))
    conn.commit()
    r.set(content['id'], content['name'])
    return 'Data added', 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)