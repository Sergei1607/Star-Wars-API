"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favorites
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    data = jsonify(Planets.get_planets())
    return data

@app.route('/characters', methods=['GET'])
def get_characters():
    data = jsonify(Characters.get_characters())
    return data


@app.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user1 = User(email=email, password=password, is_active=True)
    db.session.add(user1)
    db.session.commit()

    return jsonify({"msg":"User added"}), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password = password).first()
    if user is None:
        return jsonify({"msg":"Bad Username or Password"}), 401

    access_token = create_access_token(identity = user.id)
    return jsonify({"token" : access_token}), 200

@app.route("/addfavoriteplanet", methods=["POST"])
@jwt_required()
def addfavoriteplanet():
    current_user_id = get_jwt_identity()
    planet = request.json.get("planetid", None)

    favorite = Favorites(user_id=current_user_id, planet_id=planet)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg" : "Favorite planet added"})

@app.route("/addfavoritecharacter", methods=["POST"])
@jwt_required()
def addfavoritecharacter():
    current_user_id = get_jwt_identity()
    character = request.json.get("characterid", None)

    favorite = Favorites(user_id=current_user_id, character_id=character)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg" : "Favorite character added"})

@app.route("/getfavorites", methods=["GET"])
@jwt_required()
def getfavorites():
    current_user_id = get_jwt_identity()

    all_favorites = Favorites.query.filter_by(user_id=current_user_id)

    all_favorites = list(map(lambda x: x.serialize(), all_favorites))
           
    return jsonify(all_favorites)

@app.route("/deletefavoriteplanet", methods=["DELETE"])
@jwt_required()
def deletefavoriteplanet():
    current_user_id = get_jwt_identity()
    planet = request.json.get("planetid", None)
    planet1 = Favorites.query.filter_by(user_id=current_user_id, planet_id=planet).delete()
    db.session.commit()
           
    return jsonify({"msg" : "Favorite planet deleted"})

@app.route("/deletefavoritecharacter", methods=["DELETE"])
@jwt_required()
def deletefavoritecharacter():
    current_user_id = get_jwt_identity()
    character = request.json.get("characterid", None)
    character = Favorites.query.filter_by(user_id=current_user_id, character_id=character).delete()
    db.session.commit()
           
    return jsonify({"msg" : "Favorite character deleted"})


# this only runs if `$ python src/main.py` is executed
if __name__ =='__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
