const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const { exec } = require('child_process');

const app = express();
app.use(bodyParser.json());

// Simple in-memory DB for demo
const db = new sqlite3.Database(':memory:');
db.serialize(() => {
  db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)");
  db.run("INSERT INTO users (username, password) VALUES ('alice','password123')");
});

// 1) SQL Injection (unsafe string concat)
app.get('/user', (req, res) => {
  const username = req.query.username || '';
  const query = `SELECT * FROM users WHERE username = '${username}'`; // ❌ vulnerable
  db.all(query, (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// 2) Command injection via exec
app.get('/ping', (req, res) => {
  const host = req.query.host || '';
  exec('ping -c 1 ' + host, (error, stdout, stderr) => { // ❌ vulnerable
    if (error) return res.status(500).json({ error: stderr || error.message });
    res.json({ out: stdout });
  });
});

// 3) Dangerous eval usage
app.post('/eval', (req, res) => {
  const code = req.body.code || '';
  try {
    const result = eval(code); // ❌ dangerous
    res.json({ result });
  } catch (e) {
    res.status(400).json({ error: String(e) });
  }
});

// 4) Hardcoded secret
const API_KEY = "hardcoded-api-key-123"; // ❌ will be flagged by secret scanners
app.get('/secret', (req, res) => {
  res.json({ key: API_KEY });
});

app.get('/', (req, res) => res.send('Hello from vulnerable Node app'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server listening on ${PORT}`));
