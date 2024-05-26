from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)
    

class Player(db.Model):
    __tablename__ = "players"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    value: so.Mapped[float] 
    registered: so.WriteOnlyMapped["RegisteredPlayer"] = so.relationship(back_populates="player")
    red_team: so.WriteOnlyMapped["RedTeamPlayer"] = so.relationship(back_populates="player")
    yellow_team: so.WriteOnlyMapped["YellowTeamPlayer"] = so.relationship(back_populates="player")

    def __repr__(self):
        return "<Player {}>".format(self.name)


class RegisteredPlayer(db.Model):
    __tablename__ = "registered_players"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    player: so.Mapped[Player] = so.relationship(back_populates="registered")

    def __repr__(self):
        return "<Registered Player {}>".format(self.player_id)


class RedTeamPlayer(db.Model):
    __tablename__ = "red_team_players"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    player: so.Mapped[Player] = so.relationship(back_populates="red_team")

    def __repr__(self):
        return "<Red Team Player {}>".format(self.player_id)


class YellowTeamPlayer(db.Model):
    __tablename__ = "yellow_team_players"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    player: so.Mapped[Player] = so.relationship(back_populates="yellow_team")

    def __repr__(self):
        return "<Yellow Team Player {}>".format(self.player_id)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
