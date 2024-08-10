from flask import Flask, request, jsonify
import psycopg2
import redis

app = Flask(__name__)
 
# PostgreSQL connection
conn = psycopg2.connect(dbname="yourdbname", user="youruser", password="yourpassword", host="yourdbhost")
cur = conn.cursor()

# Redis connection
r = redis.Redis(host='yourredishost', port=6379, db=0)

@app.route('/data', methods=['GET'])
def get_data():
    cur.execute("SELECT * FROM yourtable")
    data = cur.fetchall()
    return jsonify(data)

@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json['data']
    cur.execute("INSERT INTO yourtable (column_name) VALUES (%s)", (new_data,))
    conn.commit()
    return jsonify({"message": "Data added!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)