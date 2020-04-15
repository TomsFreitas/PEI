
from flask_backend.database.db_schemas import *
from flask_backend.database.db_models import *
from flask import jsonify
from flask_backend.data_processing import isClose, same_timestamp
from flask_backend import db, login_manager


def add_video_to_database(id,url):

    accident = get_accident_by(id,filter="video_id")
       
    accident.video_location = url

    db.session.commit()

    return accident_schema.jsonify(accident)

def add_accident_to_database(accident,car):

    db.session.add(accident)
    db.session.commit()
    car.accident_id = accident.id
    db.session.add(car)
    db.session.commit()
    

def get_accident_by(value,**options):

    filter = options.get("filter")

    if filter == "belongs":
        result = Accident.query.all()
        for accident in result:
            lat = float(accident["location"]["lat"])
            lng = float(accident["location"]["lng"])
            timestamp = accident["date"]
            if isClose(value,(lat,lng)) and same_timestamp(timestamp):
                return Accident.query.filter_by(location=value).first() 

        return None

    if filter == "video_id":
        accident = Accident.query.filter_by(video_id=value).first()

        if not accident:
            return None
        
        return accident

    if filter == "all":
        all_accidents = Accident.query.all()
        result = accidents_schema.dump(all_accidents)
        return jsonify(result)
        
    if filter == "id":
        accident = Accident.query.get(value)
        return accident_schema.jsonify(accident)


#Login queries

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
