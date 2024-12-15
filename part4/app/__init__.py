from flask import Flask, Blueprint
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import config
import os
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from .config import config

bcrypt = Bcrypt()

<<<<<<< HEAD
=======

>>>>>>> 20d263bc01d8c17d7f76827a7e4b620acb8acc45
# Create Blueprint for API
api_bp = Blueprint('api', __name__)
api = Api(api_bp,
    version='1.0',
    title='HBnB API',
    description='HBnB Application API Documentation',
    doc='/docs',
)

def create_app(config_name='default'):
    """ method used to create an app instance """
<<<<<<< HEAD
    app = Flask(__name__,
                static_url_path='/static', # This makes static files serve from root
                static_folder='static', # Directory for static files
                # template_folder='templates' # Directory for HTML files
    )

    # Enable debug mode to see detailed errors
    app.config['DEBUG'] = True
=======
    app = Flask(__name__)
>>>>>>> 20d263bc01d8c17d7f76827a7e4b620acb8acc45

    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions
    CORS(app, supports_credentials=True)
    bcrypt.init_app(app)

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register web routes blueprint
    from app.routes import app as routes_bp
    app.register_blueprint(routes_bp)

    # Register routes blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register routes blueprint
    from app.routes import app as routes_bp
    app.register_blueprint(routes_bp)

    return app
