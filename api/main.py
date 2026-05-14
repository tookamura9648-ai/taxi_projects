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
import os
from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Vercelに登録した「名前」で呼び出します
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    try:
        # Supabaseの 'reservations' テーブルに保存
        supabase.table('reservations').insert({
            "name": data['name'],
            "pickup_time": data['time'],
            "equipment": data['equipment'],
            "lat": data['coords']['lat'],
            "lng": data['coords']['lng'],
            "status": "pending"
        }).execute()
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

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
