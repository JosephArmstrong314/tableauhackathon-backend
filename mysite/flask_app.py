from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import create_engine
import random
import pandas as pd
import json

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="linktreeapianaly",
    password="9847nwe8umfoiewunx9r83",
    hostname="linktreeapianalytics.mysql.pythonanywhere-services.com",
    databasename="linktreeapianaly$fifthdb",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

db_engine = SQLALCHEMY_DATABASE_URI

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
    country = db.Column(db.String(512))
    region = db.Column(db.String(512))
    city = db.Column(db.String(512))
    startTime = db.Column(db.String(512))
    endTime = db.Column(db.String(512))
    clicked = db.Column(db.Boolean)
    converted = db.Column(db.Boolean)
    inboundLink = db.Column(db.String(4096))

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

# routes
@app.route("/upload_csv", methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return 'No file provided', 400
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    if file and file.filename.endswith('.csv'):
        csv_data = pd.read_csv(file)
        csv_data.to_sql(name='test_one',con=db_engine,if_exists='replace')
        return 'CSV file uploaded and stored in SQL database successfully', 200
    else:
        return 'Invalid file type. Please upload a CSV file', 400

@app.route("/test", methods=["POST"])
def test():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    new_data = Visit(
        ipAddress = "TEST",
        country = "TEST",
        region = "TEST",
        city = "TEST",
        startTime = "TEST",
        endTime = data["timestamp"],
        clicked = 0,
        converted = 0,
        inboundLink = "TEST"
    )
    db.session.add(new_data)
    db.session.commit()
    response = jsonify({"message": "new test visit added"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Origin")
    response.headers.add("Access-Control-Max-Age", 86400)
    response.headers.add("Permissions-Policy", "unload")
    return response, 200


@app.route("/links", methods=["GET","POST","OPTIONS"])
def links():
    if (request.method == "OPTIONS"):
        response = jsonify({"message": "Preflight Request Successful! YAY!"})
    elif (request.method == "GET"):
        links = Link.query.all()
        all_links = []
        for link in links:
            all_links.append(
                {
                    "id": link.id,
                    "clicks": link.clicks
                }
            )
        response = jsonify(all_links)
    else: # POST
        data = request.get_json()
        new_link = Link(
            clicks = data["clicks"]
        )
        db.session.add(new_link)
        db.session.commit()
        response = jsonify({"message": "new link added"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Origin")
    response.headers.add("Access-Control-Max-Age", 86400)
    response.headers.add("Permissions-Policy", "unload")
    return response, 200

@app.route("/visits", methods=["GET","POST","OPTIONS", "PUT"])
def visits():
    if (request.method == "OPTIONS"):
        response = jsonify({"message": "Preflight Request Successful! YAY!"})
    elif (request.method == "GET"):
        visits = Visit.query.all()
        all_visits = []
        for visit in visits:
            all_visits.append(
                {
                    "id": visit.id,
                    "ipAddress": visit.ipAddress,
                    "country": visit.country,
                    "region": visit.region,
                    "city": visit.city,
                    "startTime": visit.startTime,
                    "endTime": visit.endTime,
                    "clicked": visit.clicked,
                    "converted": visit.converted,
                    "inboundLink": visit.inboundLink
                }
            )
        response = jsonify(all_visits)
    elif (request.method == "PUT"):
        new_end_time = request.json.get('new_end_time')
        row_id = request.json.get('row_id')
        row_to_update = Visit.query.filter_by(id=row_id).first()
        if row_to_update:
            old_endtime = row_to_update.endTime
            row_to_update.endTime = new_end_time
            db.session.commit()
            response = jsonify({'message': 'EndTime updated successfully',
                                "other message": old_endtime,
                                "last message": new_end_time,
                                "row": str(row_id)})
        else:
            response = jsonify({'message': 'Row not found'})
    else: # POST
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
            inboundLink = data["referrer"]
        )
        db.session.add(new_visit)
        db.session.commit()
        recently_added_row = Visit.query.order_by(Visit.id.desc()).first()
        response = jsonify({"message": "new visit added", "new_row_id": recently_added_row.id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Origin")
    response.headers.add("Access-Control-Max-Age", 86400)
    response.headers.add("Permissions-Policy", "unload")
    return response, 200


