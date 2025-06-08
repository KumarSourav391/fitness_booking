from . import db

class FitnessClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    datetime_ist = db.Column(db.DateTime)
    instructor = db.Column(db.String(50))
    available_slots = db.Column(db.Integer)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_class.id'))
    client_name = db.Column(db.String(50))
    client_email = db.Column(db.String(120))
    fitness_class = db.relationship('FitnessClass')