from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import *
import os

app = Flask(__name__)
#app.config.update(SERVER_NAME='localhost:5010')
DB_PATH = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/register.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH  # 'sqlite:////tmp/register.db'
db = SQLAlchemy(app)


class Filia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    SF_id = db.Column(db.Integer, db.ForeignKey('SF.id'))

class SF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    regnumb = db.Column(db.Integer, unique=True)
    datereg = db.Column(db.Date)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    Filias = db.relationship('Filia', backref = 'SF', lazy = 'dynamic')

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    surname = db.Column(db.String(200), unique=True)
    SFs = db.relationship('SF', backref = 'Person', lazy = 'dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(200), unique=True)
    street = db.Column(db.String(200), unique=True)
    house = db.Column(db.String(20), unique=True)
    SFs = db.relationship('SF', backref = 'Address', lazy = 'dynamic')

@app.route('/')
def index():
    return render_template('Index.html')

if __name__ == '__main__':

    mr_manager = APIManager(app, flask_sqlalchemy_db=db)
    mr_manager.create_api(Person, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    mr_manager.create_api(Address, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    mr_manager.create_api(SF, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    mr_manager.create_api(Filia, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    app.run(host='127.0.0.1', port=5010)
    # print(DB_PATH)