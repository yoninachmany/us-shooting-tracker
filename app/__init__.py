from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models


@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'Store': models.Store}


@app.cli.command()
def populate():
    models.Store.add_sweetgreen_geojson_data()