from app import create_app
import os

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=app.config['DEBUG'], port=port, host='0.0.0.0')
