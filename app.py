from flask import Flask, request, redirect, render_template
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "notes.db"

# Initialize DB
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

init_db()

# Home page: view + add notes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note_content = request.form["note"]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (note_content,))
        conn.commit()
        conn.close()
        return redirect("/")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    return render_template("index.html", notes=notes)

# Delete note
@app.route("/delete/<int:note_id>")
def delete(note_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Edit note
@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if request.method == "POST":
        new_content = request.form["note"]
        cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (new_content, note_id))
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        conn.close()
        return render_template("edit.html", note=note)

if __name__ == "__main__":
    app.run(debug=True)
