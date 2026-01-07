
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import db

class Game(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    started: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __repr__(self):
        return self.title