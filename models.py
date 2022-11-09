from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
db=SQLAlchemy(app)
migrate=Migrate(app, db)

class Dealer (db.Model):
    __tablename__ = 'skodadealers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    
    def __init__(self, name, city):
        self.name = name
        self.city = city
        
    def dealerdict(self):
        return {'name': self.name, 'city': self.city}
    
    
class Car (db.Model):
    __tablename__ = 'skodacars'
    id = db.Column(db.Integer, primary_key=True)    
    equipment = db.Column(db.String(100))
    model = db.Column(db.String(100))
    price = db.Column(db.Integer())
    
    def __init__(self, equipment, model, price):
        self.equipment = equipment
        self.model = model
        self.price = price
        
    def cardict(self):
        return {'equipment': self.equipment, 'model': self.model, 'price': self.price}    
    
if __name__ == '__main__':
    app.run()