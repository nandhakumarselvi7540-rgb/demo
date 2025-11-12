import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# ❌ Hardcoded secret (will be flagged)
SECRET_KEY = "mysecret123"

# ❌ Insecure database query (SQL Injection vulnerability)
def get_user_data(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# ❌ Command injection vulnerability
@app.route('/run', methods=['GET'])
def run_command():
    cmd = request.args.get('cmd')
    os.system(cmd)
    return f"Executed: {cmd}"

# ❌ Weak password storage (plaintext)
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    with open('users.txt', 'a') as f:
        f.write(f"{username}:{password}\n")
    return "User registered!"

if __name__ == "__main__":
    app.run(debug=True)
