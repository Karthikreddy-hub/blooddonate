from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, Regexp


class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=80)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80), Regexp(r"^[A-Za-z0-9_.-]+$")])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=254)])
    mobile = StringField("Mobile number", validators=[DataRequired(), Length(min=7, max=20), Regexp(r"^\+?[0-9][0-9\s-]{5,18}$")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=10, max=128)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="The passwords do not match.")])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])


class DonorForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(max=160)])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=1, max=120)])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=254)])
    mobile = StringField("Mobile number", validators=[DataRequired(), Length(min=7, max=20), Regexp(r"^\+?[0-9][0-9\s-]{5,18}$")])
    location = StringField("City / area", validators=[DataRequired(), Length(min=2, max=160)])
    blood_group = SelectField("Blood group", choices=[
        ("", "Select your blood group"),
        ("A+", "A positive"), ("A-", "A negative"),
        ("B+", "B positive"), ("B-", "B negative"),
        ("AB+", "AB positive"), ("AB-", "AB negative"),
        ("O+", "O positive"), ("O-", "O negative"),
    ], validators=[DataRequired()])
    gender = SelectField("Gender (optional)", choices=[
        ("Prefer not to say", "Prefer not to say"),
        ("Female", "Female"), ("Male", "Male"), ("Other", "Other"),
    ], validators=[Optional()])
    available = BooleanField("I am currently open to donation requests", default=True)
    consent = BooleanField(
        "I agree that my name and contact details may be shown to signed-in members of this directory."
    )
