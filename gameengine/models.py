from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
import json

class Base(DeclarativeBase):
    pass


class PlayersPlayGames(Base):
    __tablename__ = 'players_play_games'
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), primary_key=True)
    player: Mapped["Player"] = relationship(back_populates="games")
    game: Mapped["Game"] = relationship(back_populates="players")
    position_col: Mapped[int] = mapped_column(nullable=False, default=0) 
    position_row: Mapped[int] = mapped_column(nullable=False, default=0)
    next_move_col : Mapped[int] = mapped_column()
    next_move_row : Mapped[int] = mapped_column()
    
    def __repr__(self):
        return json.dumps({
            "player": self.player,
            "game": self.game
        })

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.player == other.player and self.game == other.game
        return False
        
class Game(Base):
    __tablename__ = 'game'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    started: Mapped[bool] = mapped_column(nullable=False, default=False)
    players: Mapped[List["PlayersPlayGames"]] = relationship(back_populates="game")
    active_turn: Mapped[int] = mapped_column(nullable=False, default=0)
    max_turn: Mapped[int] = mapped_column(nullable=False, default=0)
    nb_rows: Mapped[int] = mapped_column(nullable=False, default=0)
    nb_cols: Mapped[int] = mapped_column(nullable=False, default=0)
    
    def __repr__(self):
        return self.title
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.title == other.title
        return False
        
class Player(Base):
    __tablename__ = 'player'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    games: Mapped[List["PlayersPlayGames"]] = relationship(back_populates="player")
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.login == other.login
        return False
    
    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "login": self.login
        })