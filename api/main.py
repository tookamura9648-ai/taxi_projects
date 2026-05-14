import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

# 1. Flaskの初期化（一度だけ！）
app = Flask(__name__, template_folder='../templates')

# 2. Supabaseの設定（Vercelの環境変数から読み込む）
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- お客様用画面 ---
@app.route('/')
def index():
    return render_template('index.html')

# --- お客様からのデータ受信用API (Supabaseへ保存) ---
@app.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    try:
        # Supabaseの 'reservations' テーブルに保存
        supabase.table('reservations').insert({
            "name": data.get('name'),
            "pickup_time": data.get('time'),
            "equipment": data.get('equipment'),
            "lat": data.get('coords', {}).get('lat'),
            "lng": data.get('coords', {}).get('lng'),
            "status": "pending"
        }).execute()
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- 管理画面 (Supabaseからデータを取得して表示) ---
@app.route('/admin')
def admin():
    try:
        # SupabaseからIDの降順で全データを取得
        response = supabase.table('reservations').select("*").order("id", desc=True).execute()
        rows = response.data
        return render_template('admin.html', reservations=rows)
    except Exception as e:
        print(f"Admin Error: {e}")
        return f"管理画面の読み込みエラー: {e}", 500

# Vercel向けに明示
app = app

if __name__ == '__main__':
    # ローカル実行用
    app.run(debug=True, host='0.0.0.0', port=5000)
