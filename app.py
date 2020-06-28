import os
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


dirname = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dirname}/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL')

CORS(app)

mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from resources.message import bp_message

app.register_blueprint(bp_message)
