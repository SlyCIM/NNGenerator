from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produced = db.Column(db.Integer)
    target = db.Column(db.Integer)
    dataset_size = db.Column(db.Integer)
