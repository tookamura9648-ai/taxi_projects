from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os
app = Flask(__name__, template_folder='../templates')


# データベースの初期化
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            pickup_time TEXT,
            lat REAL,
            lng REAL,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# お客様からのデータ受信用API
@app.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    name = data.get('name')
    pickup_time = data.get('time')
    lat = data.get('coords').get('lat')
    lng = data.get('coords').get('lng')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reservations (name, pickup_time, lat, lng, created_at) VALUES (?, ?, ?, ?, ?)',
                   (name, pickup_time, lat, lng, created_at))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

# 管理画面（PCで見る画面）
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservations ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return render_template('admin.html', reservations=rows)

# お客様用画面
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

app = app