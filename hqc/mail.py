from flask_mail import Mail, Message
from flask import render_template
from hqc import app, mail
from threading import Thread


def ansy_send(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(title, recipients):
    msg = Message(
        title,
        recipients=recipients
    )
    msg.body =  render_template('admin/mail.txt')
    thr = Thread(target=ansy_send, args=[app, msg])
    thr.start()
