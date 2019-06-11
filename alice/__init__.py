from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


import alice.routes
import alice.model.models
