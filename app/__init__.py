from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import session as login_session

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)







from app import views, models