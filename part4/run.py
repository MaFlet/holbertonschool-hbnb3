from flask import Blueprint
from app import create_app

app = create_app()
main = Blueprint('main', __name__)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
