from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "keyyyyyyyyyyyyyyyyyyyy"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


@app.route("/")
def home():
    if "user" not in session:
        return render_template("index.html")
    else:
        return render_template("coorIndex.html")

@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = Users.query.filter_by(name=user).first()
        if found_user:
            session["password"] = found_user.password
        else:
            flash("New user saved!")
            usr = Users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    password = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            password = request.form["password"]
            session["password"] = password
            found_user = Users.query.filter_by(name=user).first()
            found_user.password = password
            db.session.commit()
            flash("Password Was Saved!")
        else:
            if "password" in session:
                password = session["password"]

        return render_template("user.html", password=password)
    else:
        flash("You Are Not Logged In!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You Have Been Logged Out!", "info")
    session.pop("user", None)
    session.pop("password", None)
    return redirect(url_for("login"))

@app.route("/baskt", methods=["POST", "GET"])
def baskt():
    found_basket = Basket.query.all()
    return render_template("basket.html", goods=found_basket)


@app.route("/prd/<id1>", methods=["POST", "GET"])
def prd(id1):
    found_shop = Shop.query.filter_by(id=id1).first()
    form = Basket(found_shop.id, found_shop.name)

if __name__ == "__main__":
    db.create_all()
    app.run(port=8080, host='127.0.0.1', debug=True)