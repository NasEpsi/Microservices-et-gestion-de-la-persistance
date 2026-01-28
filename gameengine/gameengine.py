import time
from venv import logger
from models import Player, Game, Base, PlayersPlayGames
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session



engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/loups")
Base.metadata.create_all(engine)
session = Session(engine)

def list_games():
    with Session(engine) as session:
        for game in session.scalars(select(Game)):
            print(f'{game.id} - {game.title}')

def enroll_a_game():
    instances_to_add = []
    player_login = input('Your login:')
    game_id = int(input('The game you want to join:'))
    player_new = Player(login=player_login)
    game_query = select(Game).where(Game.id == game_id)
    player_query = select(Player).where(Player.login == player_login)
    with Session(engine) as session:
        game = session.scalar(game_query)
        player = session.scalar(player_query)
        if not player:
            player = player_new
            instances_to_add.append(player)
        player_play_game = PlayersPlayGames(player=player, game=game)
        if game and player_play_game not in game.players:
            game.players.append(player_play_game)
            instances_to_add.append(player_play_game)
            session.add_all(instances_to_add)
        else:
            logger.warning(f'unable to add player {player} to game {game}')
        session.commit()
    
def display_gameboard(player, game):
    pass

def move(player, game, move):
    move_delta = input('Next move: ')

def still_alive(player, game):
    return False

def next_turn_available(player, game):
    return True

list_games()
enroll_a_game()

while still_alive('gael', 1):
    while not next_turn_available('gael', 1):
        time.sleep(1)
    display_gameboard('gael', 1)
    move('gael', 1)