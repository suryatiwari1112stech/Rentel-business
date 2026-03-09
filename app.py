from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():

    conn = get_db()
    rooms = conn.execute("SELECT * FROM rooms").fetchall()
    conn.close()

    return render_template("index.html", rooms=rooms)



@app.route("/room/<int:id>")
def room_detail(id):

    conn = get_db()

    room = conn.execute(
        "SELECT * FROM rooms WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("room_detail.html", room=room)



@app.route("/admin")
def admin():

    conn = get_db()

    rooms = conn.execute("SELECT * FROM rooms").fetchall()

    conn.close()

    return render_template("admin.html", rooms=rooms)



@app.route("/add", methods=["GET","POST"])
def add_room():

    if request.method == "POST":

        title = request.form["title"]
        price = request.form["price"]
        location = request.form["location"]
        description = request.form["description"]

        conn = get_db()

        conn.execute(
            "INSERT INTO rooms (title,price,location,description) VALUES (?,?,?,?)",
            (title,price,location,description)
        )

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("add_room.html")


if __name__ == "__main__":
    app.run(debug=True)RT