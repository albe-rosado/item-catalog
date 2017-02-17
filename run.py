#! env/bin/python
import os
import requests
import json
import config
from flask import Flask, render_template, redirect, url_for,request, jsonify, session, send_from_directory
from forms import CategoryForm , ItemForm
from models import db, Category, Item
from functools import wraps


app = Flask(__name__)
db.init_app(app)

# Loads the config
app.config.from_object('config')



""" 
    Auth Layer
"""
@app.route('/callback')
def callback_handling():
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
    return render_template('index.html', categories = categories, user=user)



# Add new category
@app.route('/newCategory', methods = ['GET', 'POST'])
@requires_auth
def newCategory(user):    
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name = form.name.data)
        db.session.add(category)
        db.session.commit()
        redirect(url_for('index'))
    return render_template('newCategory.html', form = form, user = user)

# Logout
@app.route('/logout')
def logout():
    session.pop('profile', None)
    return redirect('/')













if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=3000 ,debug = True)
