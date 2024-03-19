from . import db
import datetime

class Mega(db.Model):
    id = db.Column(db.Integer, primary_key = True)  #primary key gives each task a new id
    staff = db.Column(db.String(30), unique = True) #task to have a max entry of 300 characters and task must be unique
    transaction_type = db.Column(db.String(30), default = False)
    basket = db.Column(db.String, default = False)
    cost = db.Column(db.Integer)
    payment_method = db.Column(db.String(30), default = False)
    date_created = db.Column(db.String(10), default=datetime.date.today().strftime('%d-%m-%Y'))
    
    # priority = db.Column(db.String, default = False)
    # category = db.Column(db.String, default = False)

