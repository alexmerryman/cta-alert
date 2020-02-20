from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    station_id = StringField('Station ID:', validators=[DataRequired()])
    input_phone_num = StringField('Phone Number:', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

