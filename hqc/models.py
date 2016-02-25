import datetime
from flask import url_for
from hqc import db
from wtforms.validators import Email


class Reply(db.EmbeddedDocument):
    """define doucument of replies

    """
    author = db.StringField(max_length=255, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(require=True)


class Message(db.DynamicDocument):
    """define document of messages

    """
    msg_id = db.IntField(require=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    email = db.StringField(max_length=255, required=True, validators=[Email()])
    is_show = db.BooleanField(default=True)
    body = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=50))
    replies = db.ListField(db.EmbeddedDocumentField('Reply'))

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'ordering': ['-created_at']
    }
