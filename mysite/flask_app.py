from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="linktreeapianaly",
    password="9847nwe8umfoiewunx9r83",
    hostname="linktreeapianalytics.mysql.pythonanywhere-services.com",
    databasename="linktreeapianaly$fourthdb",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Link(db.Model):
    __tablename__ = "links"

    def __init__(self, clicks):
        self.clicks = clicks

    id = db.Column(db.Integer, primary_key = True)
    clicks = db.Column(db.Integer)

class Visit(db.Model):
    __tablename__ = "visits"

    def __init__(self, ipAddress, country, region, city, startTime, endTime, clicked, converted, inboundLink):
        self.ipAddress = ipAddress
        self.country = country
        self.region = region
        self.city = city
        self.startTime = startTime
        self.endTime = endTime
        self.clicked = clicked
        self.converted = converted
        self.inboundLink = inboundLink

    id = db.Column(db.Integer, primary_key = True)

    ipAddress = db.Column(db.String(32))
    country = db.Column(db.String(4096))
    region = db.Column(db.String(4096))
    city = db.Column(db.String(4096))

    startTime = db.Column(db.Integer)
    endTime = db.Column(db.Integer)

    clicked = db.Column(db.Boolean)
    converted = db.Column(db.Boolean)
    inboundLink = db.Column(db.String(4096))

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

# routes
@app.route("/blob", methods=["POST", "GET"])
def blob():
    data = request.get_json()
    new_link = Link(
        clicks = data["clicks"]
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": "Link created by blob"}), 200

@app.route("/strawberry", methods=["POST", "GET"])
def strawberry():
    link = Link(random.randrange(1,100000))
    db.session.add(link)
    db.session.commit()
    return jsonify({"message": "Link created by strawberry"}), 200

@app.route("/blue", methods=["POST", "GET"])
def blue():
    new_visit = Visit("123:456:1234", "America", "California", "Sacramento", 1234567, 1234599, 1, 0, "dummy link")
    db.session.add(new_visit)
    db.session.commit()
    return jsonify({"message": "new visit added"}), 200


@app.route("/link", methods=["POST"])
def add_new_link():
    data = request.get_json()
    new_link = Link(
        clicks = data["clicks"]
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": "new link added"}), 200

@app.route("/visit", methods=["POST"])
def add_new_visit():
    data = request.get_json()
    new_visit = Visit(
        ipAddress = data["ipAddress"],
        country = data["country"],
        region = data["region"],
        city = data["city"],
        startTime = data["startTime"],
        endTime = data["endTime"],
        clicked = data["clicked"],
        converted = data["converted"],
        inboundLink = data["inboundLink"]
    )
    db.session.add(new_visit)
    db.session.commit()
    return jsonify({"message": "new visit added"}), 200

@app.route("/link", methods=["GET"])
def get_all_links():
    pass

@app.route("/visit", methods=["GET"])
def get_all_visits():
    pass



