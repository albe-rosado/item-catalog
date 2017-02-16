#! env/bin/python
from flask import Flask, render_template, redirect, url_for
from forms import CategoryForm , ItemForm
from models import db, Category, Item


app = Flask(__name__)

db.init_app(app)

# Loads the config
app.config.from_object('config')



# Home
@app.route('/')
def index():
    return render_template('index.html')



# Add new category
@app.route('/newCategory', methods = ['GET', 'POST'])
def newCategory():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name = form.name.data)
        db.session.add(category)
        db.session.commit()
        redirect(url_for('index'))
    return render_template('newCategory.html', form = form)






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)