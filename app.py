"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)

@app.route('/')
def show_page():
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    """Returns JSON of all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes )

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    specific_cupcake = Cupcake.query.get_or_404(id)
    serialized = specific_cupcake.serialize()
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    try:
        new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    except:
        new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'])
    db.session.add(new_cupcake)
    db.session.commit()
    return jsonify(cupcake=new_cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify (cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods = ['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(msg = "deleted")