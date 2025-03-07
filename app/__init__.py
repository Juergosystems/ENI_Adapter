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
                error = "Request body is missing"
                response = jsonify({"message_id": None, "status": error})
                app.logger.error(response)
                return response, 400
            
            # Check if the request body is JSON
            if not request.is_json:
                error = "Request Content-Type must be JSON"
                response = jsonify({"message_id": None, "status": error})
                app.logger.error(response)
                return response, 400

            #Check if the request body is a valid JSON
            if request.get_json(silent=True) is None:
                error = "No valid JSON body found in the request"
                response = jsonify({"message_id": None, "status": error})
                app.logger.error(response)
                return response, 400
            
            # Parse the JSON body of the ENI message
            message = request.get_json(silent=True)

            if message["data"]["objectType"] == 'alertStateChange':
                info = "Alert message received"
                response = jsonify({"message_id": message["id"], "status": info})
                app.logger.info(response)
                alh = AlertHandler(message)
                return alh.routing()
            
            elif message["data"]["objectType"] == 'assessmentStateChange':
                info = "Assessment message received"
                response = jsonify({"message_id": message["id"], "status": info})
                app.logger.info(response)
                ash = AssessmentHandler(message)
                return ash.routing()
            
            else:
                return 'Bad Request', 400
        else:
            return 'Method Not Allowed', 405

    return app