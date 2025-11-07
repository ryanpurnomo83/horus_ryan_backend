import os 
from supabase import create_client , Client
from flask import Flask, request, jsonify

app = Flask(__name__)


url: str = "https://otkvvqgnyojmuwagbbpq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90a3Z2cWdueW9qbXV3YWdiYnBxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0NTMzNjQsImV4cCI6MjA3ODAyOTM2NH0.c_cH8fntvWoB5wI2m6ETFz2pVZedPSOoUBKEh5rGZrs"
supabase: Client = create_client(url, key)

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
    username = data.get("username"),
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
    return jsonify({
        "message" : "Login berhasil",
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


@app.put("/users/{id}")
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


@app.delete("/users/{id}")
def delete_user(id):
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
    }).execute()
    
    return jsonify(response.data), 200


if __name__ == "__main__":
    app.run(debug=True)
    

# https://otkvvqgnyojmuwagbbpq.supabase.co
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90a3Z2cWdueW9qbXV3YWdiYnBxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0NTMzNjQsImV4cCI6MjA3ODAyOTM2NH0.c_cH8fntvWoB5wI2m6ETFz2pVZedPSOoUBKEh5rGZrs