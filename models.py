from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Dealer (db.Model):
    __tablename__ = 'skoda_dealers'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __init__(self, name, city):
        self.name = name
        self.city = city

    def dealerdict(self):
        return {'name': self.name, 'city': self.city}
    
    def __repr__(self):
        return f"<{self.id}, {self.name}, {self.city}>"


skodadealers_cars = db.Table("skodadealers_cars",
    db.Column('dealers_id', db.Integer(), db.ForeignKey('skoda_dealers.id')),
    db.Column('cars_id', db.Integer(), db.ForeignKey('skoda_cars.id'))
    )


class Car (db.Model):
    __tablename__ = 'skoda_cars'
    id = db.Column(db.Integer(), primary_key=True)
    equipment = db.Column(db.String(100))
    model = db.Column(db.String(100))
    price = db.Column(db.Integer())
    dealers = db.relationship('Dealer', secondary = skodadealers_cars, backref = 'cars')

    def __init__(self, equipment, model, price):
        self.equipment = equipment
        self.model = model
        self.price = price

    def cardict(self):
        return {'equipment': self.equipment, 'model': self.model, 'price': self.price}

    def __repr__(self):
        return f"<{self.id}, {self.equipment}, {self.model}, {self.price}>"
