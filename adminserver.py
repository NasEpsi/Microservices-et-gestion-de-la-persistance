from flask import Flask, render_template, redirect, url_for
from flask import request

from models import Game
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:password@localhost:5432/loups"
    
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/games")
def games():
    list_games = db.session.execute(db.select(Game).order_by(Game.title)).scalars()
    return render_template("games.html", games=list_games)

@app.route('/game/<int:game_id>/stop')
def stop_game(game_id):
    game_to_stop= db.get_or_404(Game, game_id)
    game_to_stop.started = False
    db.session.add(game_to_stop)
    db.session.commit()
    return redirect(url_for("games"))

@app.route('/game/<int:game_id>/start')
def start_game(game_id):
    game_to_start= db.get_or_404(Game, game_id)
    game_to_start.started = True
    db.session.add(game_to_start)
    db.session.commit()
    return redirect(url_for("games"))

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
            