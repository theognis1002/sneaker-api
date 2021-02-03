# Sneaker API

Technologies: Flask, Marshmallow, SQLite.

Information about sneaker brand, size, quantity, and sales can be queried through a Flask API using Marshmallow as a serializer. The backend is powered by SQLite. It is recommended that a relational database should be implemented in a production environment instead.

### Development Setup

1. `virtualenv venv`
1. `source venv/bin/activate` or `venv/Scripts/activate`
1. `pip install -r requirements.txt`
1. `export FLASK_APP=app.py`
1. `flask run`
