from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


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
