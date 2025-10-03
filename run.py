from app import create_app
import logging

if __name__ == '__main__':
    logging.info('Starting Flask server on port 5050...')
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5050)