import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'cHkn3wu7se1c5gVc'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')



""" 
        Constants for Auth0 Login
"""
CODE_KEY = 'code'
CONTENT_TYPE_KEY = 'content-type'
ACCESS_TOKEN_KEY = 'access_token'
APP_JSON_KEY = 'application/json'
AUTH0_DOMAIN = 'udacity-itemcatalog.auth0.com'
AUTH0_CLIENT_ID = 'sQLcidME4R6z1UdBtYB0V4ay9pwDRoML'
AUTH0_CLIENT_SECRET = 'fcBH3ig-sBQCgggi2m4oE6jixIFk8caKWZFCNa36u2T7mKOyfNX92VfGG7fV3H5k'
AUTH0_CALLBACK_URL = 'http://localhost:3000/callback'



"""
        Constants for Algolia Search 
"""

ALGOLIA_CLIENT_ID = 'DWCAC7LUJZ'
ALGOLIA_CLIENT_SECRET = '1bb62fb76043db09505a5171a0e59dfb'
ALGOLIA_INDEX_NAME = 'ItemCatalog'