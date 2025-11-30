from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, PondLog

app = Flask(__name__)
CORS(app)

engine = create_engine('sqlite:///pond.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/logs', methods=['POST'])
def add_log():
    data = request.json
    session = Session()
    log = PondLog(ph=data['ph'], ec=data['ec'], do=data['do'], temp=data['temp'])
    session.add(log)
    session.commit()
    return jsonify({"message": "Log added"}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    session = Session()
    logs = session.query(PondLog).all()
    return jsonify([{
        "id": l.id,
        "timestamp": l.timestamp.isoformat(),
        "ph": l.ph,
        "ec": l.ec,
        "do": l.do,
        "temp": l.temp
    } for l in logs])

@app.route('/')
def home():
    return "Pond Logger API is running. Try /logs"
