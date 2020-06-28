import os

from flask import Blueprint, request, jsonify, escape
from flask_mail import Message as MessageMail

from model.message import Message
from ext.database import db
from ext.mail import mail


bp_message = Blueprint('message', __name__)


@bp_message.route('/', methods=['GET'])
def home():
    return '<h1>home</h1>'


@bp_message.route('/message/', methods=['GET'])
def all():
    try:
        messages = Message.query.all()
        data = {
            'message': [],
            'info': [
                {
                    'records':  len(messages)
                }
            ]
        }

        for message in messages:
            data['message'].append(
                {
                    'id': message.id,
                    'name': message.name,
                    'email': message.email,
                    'message': message.message,
                    'created_at': message.created_at
                }
            )

    except Exception as error:
        return {'error': str(error)}, 500

    return jsonify(data)


@bp_message.route('/message/', methods=['POST'])
def register():
    request.get_json(force=True)
    request_json = request.json

    name = escape(request_json.get('name'))
    email = request_json.get('email')
    message = escape(request_json.get('message'))

    try:
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        message_mail = MessageMail(
            'Portfolio Contato',
            recipients=[os.environ.get('EMAIL_TO')],
            body=message,
        )

        mail.send(message_mail)
        data = {'status': 'success'}

    except Exception as error:
        return {'error': str(error)}, 500

    return jsonify(data), 201


@bp_message.route('/message/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()
        data = {'message': 'Message deleted'}
    except Exception as error:
        return {'error': str(error)}, 500

    return jsonify(data), 204


@bp_message.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
