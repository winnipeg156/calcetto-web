from flask import render_template, redirect, flash, url_for
from app import app, db
from app.forms import PartecipateForm, CleanUpForm, AddPlayerForm, EditValueForm, MakeTeamsForm
import sqlalchemy as sa
from app.models import Player, RegisteredPlayer, RedTeamPlayer, YellowTeamPlayer
from app.team_maker import make_teams


@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    query = sa.select(Player)
    players = db.session.scalars(query)
    query = sa.select(RegisteredPlayer)
    registered_players = db.session.scalars(query)
    query = sa.select(RedTeamPlayer)
    red_players = db.session.scalars(query).all()
    query = sa.select(YellowTeamPlayer)
    yellow_players = db.session.scalars(query).all()
    form = PartecipateForm()
    form.name.choices = [(player.name) for player in players]
    if form.validate_on_submit(): 
        for rp in registered_players:
            if form.name.data == rp.player.name:
                return render_template("error.html")
        query = sa.select(Player).where(Player.name == form.name.data)
        p = db.session.scalars(query).first()
        rp = RegisteredPlayer(player=p)
        db.session.add(rp)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html", players=players, registered_players=registered_players,
                           form=form, red_players=red_players, yellow_players=yellow_players)


@app.route("/clean_up", methods = ["POST"])
def clean_up():
    clean_up_form = CleanUpForm()
    if clean_up_form.validate_on_submit:
        query = sa.select(RegisteredPlayer)
        registered_players = db.session.scalars(query).all()
        for rp in registered_players:
            db.session.delete(rp)
        db.session.commit()
    return redirect(url_for("admin"))


@app.route("/admin", methods = ["GET", "POST"])
def admin():
    query = sa.select(Player)
    players = db.session.scalars(query).all()
    query = sa.select(RegisteredPlayer)
    registered_players = db.session.scalars(query).all()
    clean_up_form = CleanUpForm()
    add_player_form = AddPlayerForm()
    edit_value_form = EditValueForm()
    make_teams_form = MakeTeamsForm()
    edit_value_form.name.choices = [(player.name) for player in players]
    if add_player_form.submit2.data and add_player_form.validate():
        new_player = Player(name=add_player_form.name.data, 
                            value=float(add_player_form.value.data))
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("admin"))
    if edit_value_form.submit3.data and edit_value_form.validate():
        query = sa.select(Player).where(Player.name == edit_value_form.name.data)
        p = db.session.scalars(query).first()
        p.value = float(edit_value_form.value.data)
        db.session.commit()
        return redirect(url_for("admin"))
    return render_template("admin.html", registered_players=registered_players, players=players,
                           clean_up_form=clean_up_form, add_player_form=add_player_form,
                           edit_value_form=edit_value_form, make_teams_form=make_teams_form)


@app.route("/teams", methods = ["POST"])
def teams():
    make_teams_form = MakeTeamsForm()
    if make_teams_form.validate_on_submit():
        query = sa.select(RedTeamPlayer)
        red_players = db.session.scalars(query).all()
        query = sa.select(YellowTeamPlayer)
        yellow_players = db.session.scalars(query).all()
        for player in red_players:
            db.session.delete(player)
            db.session.commit()
        for player in yellow_players:
            db.session.delete(player)
            db.session.commit()
        query = sa.select(RegisteredPlayer)
        registered_players = db.session.scalars(query).all()
        red_team, yellow_team, red_strength, yellow_strength, delta =\
                make_teams(registered_players)
        for player in red_team:
            query = sa.select(Player).where(Player.id == player.player_id)
            p = db.session.scalars(query).first()
            red_player = RedTeamPlayer(player=p, player_id=p.id)
            db.session.add(red_player)
            db.session.commit()
        for player in yellow_team:
            query = sa.select(Player).where(Player.id == player.player_id)
            p = db.session.scalars(query).first()
            yellow_player = YellowTeamPlayer(player=p)
            db.session.add(yellow_player)
            db.session.commit()
    return redirect(url_for("admin")) 


