from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from models import Category


class CategoryForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])


class ItemForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    description = TextAreaField('Description:', validators=[DataRequired()])
    cat_name = SelectField('Category:')
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.cat_name.choices = [(c.name, c.name) for c in Category.query.order_by('name')]