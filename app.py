from flask import Flask, request
from flask_restful import Api, Resource
# from models import db, Dealer, Car, skodadealers_cars
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://igar:o960xa@127.0.0.1/dbigar'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://igar:o960xa@postgres/dbigar'

db = SQLAlchemy()

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()
    
class Dealer(db.Model):
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


class Car(db.Model):
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

    def get_dict(self):
        # get_dict
        return {'equipment': self.equipment, 'model': self.model, 'price': self.price}

    def __repr__(self):
        return f"<{self.id}, {self.equipment}, {self.model}, {self.price}>"


class DealersView(Resource):
    
    def post(self):
        data = request.get_json()
        new_dealer = Dealer(data['name'], data['city'])
        db.session.add(new_dealer)    
        db.session.commit()
        return new_dealer.dealerdict(), 201
    
    def get(self):
        all_dealers=Dealer.query.all()
        if all_dealers:
            return {'All dealers':[x.dealerdict() for x in all_dealers]}
        return {'message':'Dealers not found'}
    
class CarsView(Resource):
    
    def post(self):
        data = request.get_json()
        # all_dealers=Dealer.query.all()
        dealers_city = Dealer.query.filter_by(city=data['city']).all()
        # dealers_city = Dealer.query.filter_by(city=data['city'] or name=data['sss']).all()
        new_car = Car(data['equipment'], data['model'], data['price'])
        for x in dealers_city:
            x.cars.append(new_car)
            db.session.add(x)
            db.session.commit()
        dealers_newcar=new_car.dealers
        return  {'New car':new_car.get_dict(), 'Dealers':list(y.dealerdict() for y in dealers_newcar)}, 201
    
    def get(self):
        all_cars = Car.query.all()
        return {'All cars':list(x.get_dict() for x in all_cars)}


class DealerView(Resource):
    
    def get(self,name):
        dealer = Dealer.query.filter_by(name=name).first()
        if dealer:
            cars = dealer.cars
            return {f'Dealer {name}':dealer.dealerdict(), 'Cars':list(x.get_dict() for x in cars)}
        
        return {'message':'Dealer not found'}, 404
    
    def put(self,name):
        data = request.get_json()
        dealer = Dealer.query.filter_by(name=name).first()
        if dealer:
            dealer.name = data['name']
            dealer.city = data['city']
            db.session.commit()
            return {'Update Dealer':dealer.dealerdict()}
        else:
            dealer = Dealer(name=name, city=data['city']) 
        
        db.session.add(dealer)
        db.session.commit()
        return {'New dealer':dealer.dealerdict()} 
    
    def delete(self,name):
        dealer = Dealer.query.filter_by(name=name).first()
        if dealer:
            db.session.delete(dealer)
            db.session.commit()
            return {'message': 'Deleted'}
        
        return {'message': 'Dealer not found'}, 404
        
        
class CarView(Resource):
    
    def get(self,model):
        car = Car.query.filter_by(model=model).first()
        if car:
            dealers = car.dealers
            return {f'Car {model}':car.get_dict(), 'Dealers':list(x.dealerdict() for x in dealers)}
    
        return {'Message': 'Car not found'}, 404
     
    def put(self, model):
        data = request.get_json()
        car = Car.query.filter_by(model=model).first()
        if car:
             car.equipment = data['equipment']
             car.model = data['model']
             car.price = data['price']
        else:
             car = Car(equipment = data['equipment'], model=model, price = data['price'])
             dealers = Dealer.query.filter_by(city=data['city']).all()
             for x in dealers:
                 x.cars.append(car)
                 db.session.add(x)
                 db.session.commit()
                 return {'New Car':car.get_dict(), 'Dealers':list(y.dealerdict() for y in dealers)}, 201    
        
        db.session.commit()
        return {'Update Car':car.get_dict()}
        
    def delete(self, model):
        car = Car.query.filter_by(model=model).first()
        if car:
            db.session.delete(car)
            db.session.commit()
            return {'Message': 'Deleted'}
        return {'Message': 'Car not found'}, 404   
                   
         
             
        
api.add_resource(DealersView, '/dealers')        
api.add_resource(CarsView, '/cars')
api.add_resource(DealerView, '/dealer/<string:name>')
api.add_resource(CarView, '/car/<string:model>')
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)         