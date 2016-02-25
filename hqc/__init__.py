from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {'DB': "test"}
app.config["SECRET_KEY"] = "hqc-203"

db = MongoEngine(app)


def register_blueprints(app):
    from hqc.views import messages
    from hqc.admin import admin
    app.register_blueprint(messages)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == "__main__":
    app.run()
