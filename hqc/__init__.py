# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {'DB': "test"}
app.config["SECRET_KEY"] = "hqc-203"
app.config.update(
    MAIL_USE_TLS = True,
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PORT = 587,
    MAIL_USERNAME = '937031218',
    MAIL_PASSWORD = 'hmansxbbjbfbbfaf',
    MAIL_DEFAULT_SENDER = '937031218@qq.com'
)


def send_email():
    msg = Message(
        '你好',
        sender='937031218@qq.com',
        recipients=['346097601@qq.com']
    )
    msg.body ="this is the email body"
    mail.send(msg)
    return "sent"



db = MongoEngine(app)
mail = Mail(app)

def register_blueprints(app):
    from hqc.views import messages
    from hqc.admin import admin
    app.register_blueprint(messages)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == "__main__":
    app.run()
