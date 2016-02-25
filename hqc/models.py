import datetime
from flask import url_for
from hqc import db


class Reply(db.Document):
    """define doucument of replies

    """
    author = db.StringField(max_length=255, request=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, require=True)
    body = db.StringField(require=True)


class Message(db.Document):
    """define document of messages

    """
    msg_id = db.IntField(require=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, require=True)
    title = db.StringField(max_length=255, require=True)
    email = db.StringField(max_length=255, require=True)
    is_show = db.BooleanField(default=False)
    body = db.StringField(require=True)
    tags = db.ListField(db.StringField(max_length=50))
    replies = db.ListField(db.EmbeddedDocumentField('Reply'))

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'ordering': ['-created_at']
    }
