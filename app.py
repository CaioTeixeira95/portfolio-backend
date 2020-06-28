import os
from flask import Flask
from flask_migrate import Migrate
from ext import database, cors, mail 


app = Flask(__name__)

cors.init_app(app)
mail.init_app(app)

database.init_app(app)
migrate = Migrate(app, database.db)

from model.message import Message
from blueprints.message import bp_message

app.register_blueprint(bp_message)
