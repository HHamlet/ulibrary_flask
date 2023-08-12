from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, NumberRange


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
