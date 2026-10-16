
import os
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "change-this-before-deployment"
)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + str(INSTANCE_DIR / "witching_hour.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    entries = db.relationship(
        "JournalEntry", backref="author",
        cascade="all, delete-orphan", lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=db.func.now()
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/grimoire")
def grimoire():
    return render_template("grimoire.html")


@app.route("/apothecary")
def apothecary():
    return render_template("apothecary.html")


@app.route("/lunar")
def lunar():
    return render_template("lunar.html")


@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        entry_id = request.form.get("entry_id", "").strip()

        if not title or not content:
            flash("Please fill in both the title and content.", "error")
            return redirect(url_for("journal"))

        if entry_id:
            entry = db.session.get(JournalEntry, int(entry_id))
            if not entry or entry.user_id != current_user.id:
                flash("Entry not found.", "error")
                return redirect(url_for("journal"))

            entry.title = title
            entry.content = content
            flash("Your entry has been updated.", "success")
        else:
            entry = JournalEntry(
                title=title,
                content=content,
                user_id=current_user.id
            )
            db.session.add(entry)
            flash("Your entry has been saved.", "success")

        db.session.commit()
        return redirect(url_for("journal"))

    entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(JournalEntry.created_at.desc()).all()

    return render_template("journal.html", entries=entries)


@app.route("/journal/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = db.session.get(JournalEntry, entry_id)

    if not entry or entry.user_id != current_user.id:
        flash("Entry not found.", "error")
        return redirect(url_for("journal"))

    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted.", "success")
    return redirect(url_for("journal"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 8:
            flash(
                "Use a username of at least 3 characters "
                "and a password of at least 8 characters.", "error"
            )
        elif User.query.filter_by(username=username).first():
            flash("That username is already taken.", "error")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("journal"))

    return render_template("login.html", registering=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("journal"))

        flash("Incorrect username or password.", "error")

    return render_template("login.html", registering=False)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
