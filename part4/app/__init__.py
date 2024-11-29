from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = secrets.token_hex(16) # generate secret key for session (Does not require JWT token)

db = SQLAlchemy(app)
bcrypt = Brcypt(app)

from app import routes
