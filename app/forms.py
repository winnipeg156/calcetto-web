from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class PartecipateForm(FlaskForm):
    name = SelectField("Nome")
    submit = SubmitField("Partecipa")


class CleanUpForm(FlaskForm):
    submit1 = SubmitField("Pulisci")


class AddPlayerForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    value = StringField("Valore", validators=[DataRequired()])
    submit2 = SubmitField("Aggiungi al DB")


class EditValueForm(FlaskForm):
    name = SelectField("Nome")
    value = StringField("Valore", validators=[DataRequired()])
    submit3 = SubmitField("Modifica valore")

class MakeTeamsForm(FlaskForm):
    submit4 = SubmitField("Fai le squadre")
