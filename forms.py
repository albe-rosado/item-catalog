from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired



class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class ItemForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    cat_assign = SelectField(u'Programming Language', choices=[('py', 'Python'), ('text', 'Plain Text')])