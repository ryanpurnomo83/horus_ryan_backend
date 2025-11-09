import os
import jwt
import datetime
from supabase import create_client , Client
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey123"

CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "http://192.168.1.4:5173", "http://192.168.1.4:8080"]}})

url: str = "https://otkvvqgnyojmuwagbbpq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90a3Z2cWdueW9qbXV3YWdiYnBxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0NTMzNjQsImV4cCI6MjA3ODAyOTM2NH0.c_cH8fntvWoB5wI2m6ETFz2pVZedPSOoUBKEh5rGZrs"
supabase: Client = create_client(url, key)

@app.route("/")
def welcome():
    flask_logo_url = url_for('static', filename='Flask_logo.png')
    horus_logo_url = url_for('static', filename='horus_logo.png')
    return f"""
    <html>
    <head>
        <title>Flask API Docs</title>
        <style>
            body {{
                font-family: "Segoe UI", Arial, sans-serif;
                background-color: #f9fafb;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            .header {{
                text-align: center;
                padding: 30px 0 5px;
                color: black;
            }}
            .header img{{
                width: 45%;
            }}
            .logo-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 40px;
                margin-top: 20px;
            }}
            .logo-container img {{
                width: 120px;
                height: auto;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
            }}
            h1 {{
                text-align: center;
                color: #444;
                margin-top: 40px;
            }}
            .docs {{
                max-width: 700px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }}
            h2 {{
                color: #ff914d;
                border-left: 5px solid #ff914d;
                padding-left: 10px;
                margin-top: 30px;
            }}
            ul {{
                list-style: none;
                padding-left: 20px;
            }}
            li {{
                background-color: #f1f3f5;
                margin: 6px 0;
                padding: 10px 15px;
                border-radius: 5px;
                font-family: monospace;
                color: #333;
            }}
            li:hover {{
                background-color: #e9ecef;
            }}
            footer {{
                text-align: center;
                margin: 40px 0;
                font-size: 14px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="{flask_logo_url}" alt="Flask Logo">
            <h1>Welcome to Flask</h1>
            <p>Interactive API Documentation</p>
        </div>

        <div class="logo-container">
            <img src="{horus_logo_url}" alt="Horus Logo">
        </div>

        <div class="docs">
            <h2>POST</h2>
            <ul>
                <li>/users/register</li>
                <li>/users/login</li>
            </ul>

            <h2>GET</h2>
            <ul>
                <li>/users/</li>
            </ul>

            <h2>PUT</h2>
            <ul>
                <li>/users/&lt;id&gt;</li>
            </ul>

            <h2>DELETE</h2>
            <ul>
                <li>/users/&lt;id&gt;</li>
            </ul>
        </div>

        <footer>
            Powered by Flask
        </footer>
    </body>
    </html>
    """

@app.post("/users/register")
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    nama = data.get("nama")
    
    if not all([username, password, email, nama]):
        return jsonify({"error": "Semua field wajib diisi"}), 400
    
    response = supabase.table("users").insert({
        "username": username,
        "password": password,
        "email": email,
        "nama": nama
    }).execute()
    
    return jsonify(response.data), 201
    
    
@app.post("/users/login")
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not all([username, password]):
        return jsonify({"error": "Semua field wajib diisi"}, 400)
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("username", username)
        .eq("password", password)
        .execute()
        )
    
    if len(response.data) == 0:
        return jsonify({"error": "Username atau password salah"}), 401
    
    user = response.data[0]
    
    payload = {
        "id" : user["id"],
        "username" : user["username"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    
    return jsonify({
        "message" : "Login berhasil",
        "token": token,
        "user" : {
            "id" : user["id"],
            "username" : user["username"],
            "email" : user["email"],
            "nama" : user["nama"]
        }    
    }), 200


@app.get("/users")
def list_user():
    response = supabase.table("users").select("*").execute()
    return jsonify({
        "status": "success",
        "count": len(response.data),
        "data": response.data
    }), 200


@app.put("/users/<int:id>")
def update_user(id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    nama = data.get("nama")
    
    if not all([username, password, email, nama]):
        return jsonify({"error": "Semua field wajib diisi"}), 400
    
    response = supabase.table("users").update({
        "username": username,
        "password": password,
        "email": email,
        "nama": nama
    }).eq("id", id).execute()
    
    return jsonify(response.data), 200


@app.delete("/users/<int:id>")
def delete_user(id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    nama = data.get("nama")
    
    if not all([username, password, email, nama]):
        return jsonify({"error": "Semua field wajib diisi"}), 400
    
    response = (
        supabase
        .table("users")
        .delete()
        .eq("id", id)
        .execute()
    )
    if len(response.data) == 0:
        return jsonify({"error": "User dengan ID tersebut tidak ditemukan"}), 404
    
    return jsonify(response.data), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    

# https://otkvvqgnyojmuwagbbpq.supabase.co
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90a3Z2cWdueW9qbXV3YWdiYnBxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0NTMzNjQsImV4cCI6MjA3ODAyOTM2NH0.c_cH8fntvWoB5wI2m6ETFz2pVZedPSOoUBKEh5rGZrs