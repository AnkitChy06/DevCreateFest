from flask import Flask
from flask_migrate import Migrate
from app import create_app
from app.models import db
import logging
import os

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)
    
    logging.info('Starting Flask server on port 5050...')
    app.run(debug=True, host='127.0.0.1', port=5050)