from flask_sqlalchemy import SQLAlchemy
import os

db: SQLAlchemy = SQLAlchemy()

POSTGRES_USER = "zgel"
POSTGRES_PASSWORD = "L+vr7lt_Oax8+Q6BE9VdmZf"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "calidadtotal"

DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def inciar_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)