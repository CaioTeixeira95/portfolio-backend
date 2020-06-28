import os
from flask_mail import Mail


mail = Mail()


def init_app(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL')
    mail.init_app(app)