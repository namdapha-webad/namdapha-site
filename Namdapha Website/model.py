from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    group_number = db.Column(db.Integer)
    city = db.Column(db.String(30))
    name = db.Column(db.String(50), nullable=True)  
    House = db.Column(db.String(50), nullable=False)  
