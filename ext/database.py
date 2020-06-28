import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    dirname = os.path.dirname(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dirname}/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
