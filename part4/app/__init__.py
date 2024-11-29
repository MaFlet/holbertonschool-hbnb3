from flask import Flask
from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)

app.secret_key = secrets.token_hex(16) # generate secret key for session (Does not require JWT token)

# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes
