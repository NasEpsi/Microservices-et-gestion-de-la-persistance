from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///adminserver.db"
    
class Game(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return self.title
    
db.init_app(app)

with app.app_context():
    db.create_all()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/games")
def games():
    list_games = db.session.execute(db.select(Game)).scalars()
    return render_template("games.html", games=list_games)

@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        title = request.form['title']
        app.logger.info(title)
        game = Game(title=title)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for("games"))
    return render_template("game.html")
            