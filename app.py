import os

from flask import Flask, jsonify, make_response, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
marsh = Marshmallow(app)


class Sneaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(200))
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, brand, year, price, qty):
        self.name = name
        self.brand = brand
        self.year = year
        self.price = price
        self.qty = qty


class SneakerSchema(marsh.Schema):
    class Meta:
        fields = ("id", "name", "brand", "year", "price", "qty")


sneaker_schema = SneakerSchema()
sneakers_schema = SneakerSchema(many=True)


@app.route("/sneaker", methods=["POST"])
def add_sneaker():
    """add new sneaker

    Returns:
        json: success message
    """
    name = request.json["name"]
    brand = request.json["brand"]
    year = request.json["year"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_sneaker = Sneaker(name, brand, year, price, qty)
    db.session.add(new_sneaker)
    db.session.commit()

    return sneaker_schema.jsonify(new_sneaker), 200


@app.route("/sneaker/<int:id>", methods=["GET", "PUT", "DELETE"])
def delete_sneaker(id):
    """get, update or delete single sneaker by id #

    Args:
        id (int): sneaker id #

    Returns:
        json: success message
    """
    sneaker = sneaker.query.get_or_404(id)

    if request.method == "GET":
        return sneaker_schema.jsonify(sneaker), 200

    elif request.method == "DELETE":
        db.session.delete(sneaker)
        db.session.commit()
        return jsonify({"message": "Successfully deleted"}), 200

    elif request.method == "PUT":
        name = request.json["name"]
        brand = request.json["brand"]
        year = request.json["year"]
        price = request.json["price"]
        qty = request.json["qty"]

        sneaker.name = name
        sneaker.brand = brand
        sneaker.year = year
        sneaker.price = price
        sneaker.qty = qty
        db.session.commit()

        return sneaker_schema.jsonify(sneaker), 200

    else:
        return jsonify({"message": "method not allowed"}), 400


@app.route("/sneakers", methods=["GET"])
def get_all_sneakers():
    """gets all sneakers in database

    Returns:
        json: list of all sneaker info from database in json format
    """
    sneakers = Sneaker.query.all()

    return sneakers_schema.jsonify(sneakers), 200


if __name__ == "__main__":
    app.run(debug=True)
