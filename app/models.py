from app import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable = False)
    item = db.relationship('Item', backref = 'category', lazy = 'dynamic')

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('category'))
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.Text, nullable = False)


# class User(db.Model):
#     """
#     # TODO:
#     Pending
#     """
#     __tablename__ = 'user'
#     pass
