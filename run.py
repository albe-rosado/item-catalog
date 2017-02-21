#! env/bin/python
import os
import requests
import json
import config
from algoliasearch import algoliasearch
from flask import Flask, render_template, redirect, url_for,request, jsonify, session, send_from_directory, jsonify
from forms import CategoryForm , ItemForm
from models import db, Category, Item
from functools import wraps


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


# Add objects to algolia index
client = algoliasearch.Client( config.ALGOLIA_CLIENT_ID, config.ALGOLIA_CLIENT_SECRET)
algolia_index = client.init_index( config.ALGOLIA_INDEX_NAME)


""" 
    Auth Layer
"""
@app.route('/callback')
def callback_handling():
    import json
    code = request.args.get(config.CODE_KEY)

    json_header = {config.CONTENT_TYPE_KEY: config.APP_JSON_KEY}

    token_url = "https://{domain}/oauth/token".format(domain=config.AUTH0_DOMAIN)

    token_payload = {
    'client_id':     config.AUTH0_CLIENT_ID,
    'client_secret': config.AUTH0_CLIENT_SECRET,
    'redirect_uri':  config.AUTH0_CALLBACK_URL,
    'code':          code,
    'grant_type':    'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain=config.AUTH0_DOMAIN, access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    # Saves all user information into the session
    session['profile'] = user_info

    # Redirect to the User logged in page 
    return redirect('/')

# Checks if the user is logged in
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' in session:
            user = session['profile']
        else:
            user = None
            # Takes him to the home page
            return redirect('/')
        return f(user = user, *args, **kwargs)
    return decorated






"""
    Views
"""

# Home
@app.route('/')
def index():
    if 'profile' in session:
        user = session['profile']
    else:
        user = None
    categories = Category.query.all()
    last_added = Item.query.order_by('id desc').limit(10)
    params = dict(categories = categories, user = user, last_added = last_added)
    return render_template('index.html', **params )




# Add new category
@app.route('/newCategory', methods = ['GET', 'POST'])
@requires_auth
def newCategory(user):
    error = None
    form = CategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            category = Category(name = form.name.data)
            db.session.add(category)
            db.session.commit()
            redirect(url_for('index'))
        else:
            error = 'All fields are required'
    params = dict(user = user, 
                  form = form,
                  error = error)
    return render_template('newCategory.html', **params)




# Add New Item 
@app.route('/newItem', methods = ['GET', 'POST'])
@requires_auth
def newItem(user):
    error = None
    form = ItemForm()
    if request.method == 'POST':        
        if form.validate_on_submit():
            if Item.query.filter_by(title = form.title.data).first():
                error = 'Item is already in our records'
            else:                
                item = Item(title = form.title.data, 
                            description = form.description.data, 
                            cat_name = form.cat_name.data,
                            created_by = user['user_id'])
                db.session.add(item)
                db.session.commit()
                # Adds new entry to Algolia's index
                algolia_index.add_objects([item.serialize])
                redirect(url_for('index'))
        else:
            error = 'All fields are required'
    params = dict(user = user, form = form, error = error)
    return render_template('newItem.html', **params)




# Shows Item details
@app.route('/category/<cat_name>/item/<item_id>')
def showItem(cat_name, item_id):
    item = Item.query.filter_by(id = item_id).first_or_404()
    if 'profile' in session:
        user = session['profile']
    else:
        user = None
    return render_template('showItem.html', item = item, user = user)




# Edit Item
@app.route('/item/<item_id>/edit', methods = ['GET', 'POST'])
@requires_auth
def editItem(item_id, user):
    item = Item.query.filter_by(id = item_id).first_or_404()
    # Checks user owns post
    if user['user_id'] != item.created_by:
        return redirect('/')
    else:
        form = ItemForm()
        message = None
        if request.method == 'POST':
            if form.validate_on_submit():
                item.title = form.title.data
                item.description = form.description.data
                db.session.commit()
            else:
                message = "All fields are required"
        params = dict(item = item, user = user, form = form)
        return render_template('editItem.html', **params)




# Remove item
@app.route('/item/<item_id>/delete', methods = ['GET', 'POST'])
@requires_auth
def deleteItem(item_id, user):
    item = Item.query.filter_by(id = item_id).first_or_404()
    # Checks user owns post
    if user['user_id'] != item.created_by:
        return redirect('/')
    else:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')




# Shows items in a category
@app.route('/category/<cat_name>')
def showCategory(cat_name):
    items = Item.query.filter_by(cat_name = cat_name).all()
    params = dict(cat_name = cat_name, items = items)
    return render_template('showCategory.html', **params)



# return item's JSON data
@app.route('/category/<cat_name>/item/<item_id>/catalog.json')
def itemJson(cat_name, item_id):
    item = Item.query.filter_by(id = item_id).first_or_404()
    return jsonify(item.serialize)




# Logout
@app.route('/logout')
def logout():
    session.pop('profile', None)
    return redirect('/')









if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=3000 ,debug = True)
