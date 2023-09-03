from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, EmailField
from wtforms.validators import InputRequired, NumberRange, EqualTo


class CreateBookForm(FlaskForm):
    book_title = StringField(
        validators=[
            InputRequired()
        ]
    )

    author_first_name = StringField(
        validators=[
            InputRequired()
        ]
    )

    author_last_name = StringField(
        validators=[
            InputRequired()
        ]
    )

    first_published_year = DecimalField(
        validators=[
            NumberRange()
        ]
    )

    isbn = StringField(validators=[])
    published_year = StringField(validators=[])


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
        ],
    )
    password = StringField(
        validators=[
            InputRequired(),
        ],
    )


class AdminRegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
        ]
    )

    user_name = StringField(
        validators=[
            InputRequired(),
        ]
    )
    user_lastname = StringField(
        validators=[]
    )
    email = EmailField(
        validators=[
            InputRequired(),
        ]
    )
    password = StringField(
        validators=[
            InputRequired(),
        ]
    )
    repeat_password = StringField(
        validators=[
            EqualTo(
                "password",
                message="Passwords don't match",
            ),
        ]
    )


class StudentRegisterForm(FlaskForm):
    first_name = StringField(
        validators=[
            InputRequired(),
        ]
    )

    last_name = StringField(
        validators=[
            InputRequired(),
        ]
    )

    email = EmailField(
        validators=[
            InputRequired(),
        ]
    )