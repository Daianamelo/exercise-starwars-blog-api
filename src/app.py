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
from models import db, User, Usuario, Personajes, Planetas, Vehiculos, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#aca empiezan los endpoints

#consulta user todos
@app.route('/user', methods=['GET'])
def handle_hello():
    allusers=User.query.all()
    print(allusers)
    results=list(map(lambda item: item.serialize(),allusers))
    # print(results)
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(results), 200

#consulta individual user

@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    # print(user_id)
    #peter = User.query.filter_by(username='peter').first()
    user= User.query.filter_by(id=user_id).first()
    # print(user.serialize())
    # allusers=User.query.all()
    # print(allusers)
    # results=list(map(lambda item: item.serialize(),allusers))
    # print(results)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(user.serialize()), 200

    #consulta planetas
#1)cambiar por el nombre que necesito y fijarme si va get o otra cosa
@app.route('/Planetas', methods=['GET'])
def info_planetas():
     allplanetas=Planetas.query.all()
     print(allplanetas)
     results=list(map(lambda item: item.serialize(),allplanetas))
     print(resultado)
     response_body = {
        "msg": "Hello, this is your GET /planet response "
     }
     return jsonify(planetas.serialize()), 200
    

#terminan endpoints
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
