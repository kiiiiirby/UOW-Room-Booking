from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, TimeField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class CreateRoomForm(FlaskForm):
    room_code_input = StringField("Room Code:", validators=[DataRequired()])
    room_price_input = IntegerField(
        "Price of Room (/hr):", validators=[DataRequired()]
    )
    room_cap_input = IntegerField(
        "Capacity of the room (Pax):", validators=[DataRequired()]
    )
    promo_code_input = StringField("Promotion Code")
    promo_code_amt_input = IntegerField("Discount (%):", default=0)
    start_date_input = DateField(
        "Enter the start date and time the room is unavailable."
    )
    start_time_input = TimeField("")
    end_date_input = DateField("Enter the start date and time the room is unavailable.")
    end_time_input = TimeField("")
    submit = SubmitField("Create Room")


class EditRoomForm(FlaskForm):
    room_price_input = IntegerField(
        "Price of Room (/hr):", validators=[DataRequired()]
    )
    room_cap_input = IntegerField(
        "Capacity of the room (Pax):", validators=[DataRequired()]
    )
    promo_code_input = StringField("Promotion Code")
    promo_code_amt_input = IntegerField("Discount (%):", default=0)
    start_date_input = DateField(
        "Enter the start date and time the room is unavailable."
    )
    start_time_input = TimeField("")
    end_date_input = DateField("Enter the start date and time the room is unavailable.")
    end_time_input = TimeField("")
    submit = SubmitField("Edit Room")


class BookRoomForm(FlaskForm):
    start_date_input = DateField("From:")
    start_time_input = TimeField("")
    end_date_input = DateField("To:")
    end_time_input = TimeField("")
    promo_code_input = StringField("Promotion Code")
    submit = SubmitField("Submit")


class EditBookingForm(FlaskForm):
    start_date_input = DateField("From:")
    start_time_input = TimeField("")
    end_date_input = DateField("To:")
    end_time_input = TimeField("")
    submit = SubmitField("Submit")
