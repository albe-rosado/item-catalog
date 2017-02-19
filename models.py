from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable = False, unique = True)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String, db.ForeignKey('categories.name'))
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.Text, nullable = False)
    created_by = db.Column(db.String)
    
    @property
    def serialize(self):

        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'belong_to_category': self.cat_name
        }

