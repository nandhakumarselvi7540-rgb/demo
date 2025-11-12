import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# 🚨 Vulnerability 1: SQL Injection
@app.route("/user")
def get_user():
    username = request.args.get("username")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Unsafe string concatenation in SQL query
    query = "SELECT * FROM users WHERE username = '" + username + "';"
    cursor.execute(query)
    result = cursor.fetchall()
    return {"result": result}


# 🚨 Vulnerability 2: Command Injection
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    os.system("ping -c 1 " + ip)  # Dangerous! Executes arbitrary commands
    return {"message": f"Pinging {ip}"}


# ✅ Safe example
@app.route("/")
def home():
    return {"message": "Hello Secure World"}

if __name__ == "__main__":
    app.run(debug=True)
