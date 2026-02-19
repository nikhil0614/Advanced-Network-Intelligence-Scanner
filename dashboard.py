from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT target, result, timestamp FROM scans")
    rows = cursor.fetchall()
    conn.close()

    scans = []
    for row in rows:
        scans.append({
            "target": row[0],
            "data": json.loads(row[1]),
            "timestamp": row[2]
        })

    return render_template("dashboard.html", scans=scans)

if __name__ == "__main__":
    app.run(debug=True)
