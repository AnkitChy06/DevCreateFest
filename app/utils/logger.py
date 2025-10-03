import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/arvora.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    
    # Set formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Set log level from config
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    
    # Log startup message
    app.logger.info('Arvora startup')