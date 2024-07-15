from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    amount = db.Column(db.Float)
    category = db.Column(db.String(100))
    tickets = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.Date)
    venue = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    description = db.Column(db.Text)
    poster = db.Column(db.String(100))
    location = db.Column(db.String(100)) 
