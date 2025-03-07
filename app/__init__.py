import os

from flask import Flask
from flask import request, jsonify
from config import Config as cfg

from app.alert_handler import AlertHandler
from app.assessment_handler import AssessmentHandler
from app.utils.logger import init_logger

def create_app(config_class=cfg.App):
    # create and configure the app
    app = Flask(__name__)

    # load the config
    app.config.from_object(config_class)

    # initialize the logger
    init_logger(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Endpoint to receive the eni messages
    @app.route('/event', methods=['POST'])
    def event():
        if request.method == 'POST':
            
            # Check if there is a request body
            if not request.data:
                error_message = "Request body is missing"
                app.logger.error(error_message)
                return jsonify({"error": error_message}), 400
            
            # Check if the request body is JSON
            if not request.is_json:
                error_message = "Request Content-Type must be JSON"
                app.logger.error(error_message)
                return jsonify({"error": error_message}), 400

            #Check if the request body is a valid JSON
            if request.get_json(silent=True) is None:
                error_message = "No valid JSON body found in the request"
                app.logger.error(error_message)
                return jsonify({"error": error_message}), 400

            message = request.get_json(silent=True)
            if message["data"]["objectType"] == 'alertStateChange':
                app.logger.info("Alert message received")
                alh = AlertHandler(message)
                return alh.routing()
            
            elif message["data"]["objectType"] == 'assessmentStateChange':
                app.logger.info("Assessment message received")
                ash = AssessmentHandler(message)
                return ash.routing()
            
            else:
                return 'Bad Request', 400
        else:
            return 'Method Not Allowed', 405

    return app