import os
import sqlite3
import smtplib

from flask import Blueprint, request, jsonify
from email.mime.text import MIMEText


bp_message = Blueprint('message', __name__, cli_group='other')


@bp_message.route('/', methods=['GET'])
def home():
    return '<h1>home</h1>'


@bp_message.route('/message/', methods=['GET'])
def all():
    try:
        connection = sqlite3.connect('portfolio.db')
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, email, message
              FROM message""")

        records = cursor.fetchall()
        data = {
            'message': [],
            'info': [
                {
                    'records':  len(records)
                }
            ]
        }

        for row in records:
            data['message'].append(
                {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'message': row[3],
                }
            )
        cursor.close()

    except sqlite3.Error as error:
        return {'error': str(error)}, 500
    finally:
        if (connection):
            connection.close()

    return jsonify(data)


@bp_message.route('/message/', methods=['POST'])
def register():
    request.get_json(force=True)
    query_parameters = request.json

    name = query_parameters.get('name')
    email = query_parameters.get('email')
    message = query_parameters.get('message')

    try:
        connection = sqlite3.connect('portfolio.db')
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO message
                (name, email, message)
            VALUES
                (?, ?, ?)
            """, (name, email, message))

        connection.commit()

        cursor.close()
        message_r = message
        data = {'status': 'success'}

        # conexão com os servidores do google
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465

        # username ou email para logar no servidor
        username = os.getenv('EMAIL')
        password = os.getenv('EMAIL_PASS')

        from_addr = os.getenv('EMAIL')
        to_addrs = [os.getenv('EMAIL_TO')]

        text = f"""Mensagem recebida: {message_r},
        De: {name} - {email}
        """
        message = MIMEText(text)
        message['subject'] = 'Mensagem do Portfolio'
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()

    except sqlite3.Error as error:
        return {'error': str(error)}, 500
    except Exception as error:
        return {'error': str(error)}, 500
    finally:
        if (connection):
            connection.close()

    return jsonify(data), 201


@bp_message.route('/message/<id>', methods=['DELETE'])
def delete(id):
    try:
        connection = sqlite3.connect('portfolio.db')
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM message WHERE id = ?""", id)
        connection.commit()
        cursor.close()
        data = {'message': 'Message deleted'}
    except sqlite3.Error as error:
        return {'error': str(error)}, 500
    finally:
        if (connection):
            connection.close()

    return jsonify(data), 204


@bp_message.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@bp_message.route('/db/migrate/', methods=['POST'])
def migrate():
    try:
        connection = sqlite3.connect('portfolio.db')
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE message (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                message TEXT
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception:
        return {'error': 'Error trying to create table.'}
    
    return {'message': 'Success'}, 200
