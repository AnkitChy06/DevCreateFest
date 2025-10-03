import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    """Set up and return a logger instance"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Only add handlers if they don't exist
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Create file handler with rotation
        file_handler = RotatingFileHandler(
            'logs/arvora.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Set overall logger level
        logger.setLevel(logging.INFO)
    
    return logger

def setup_logging(app):
    """Set up logging for the Flask application"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set up file handler with rotation
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
    
    # Set log level from config or default to INFO
    log_level = app.config.get('LOG_LEVEL', logging.INFO)
    file_handler.setLevel(log_level)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    
    # Log startup message
    app.logger.info('Arvora startup')
    file_handler.setFormatter(formatter)
    
    # Set log level from config
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    
    # Log startup message
    app.logger.info('Arvora startup')