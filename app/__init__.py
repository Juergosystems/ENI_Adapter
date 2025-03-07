import os

from flask import Flask
from flask import request
from config import Config as cfg

from app.alert_handler import AlertHandler
from app.assessment_handler import AssessmentHandler

def create_app(config_class=cfg.App):
    # create and configure the app
    app = Flask(__name__)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Endpoint to receive the eni messages
    @app.route('/event', methods=['POST'])
    def event():
        if request.method == 'POST':
            message = request.get_json()
            if message["data"]["objectType"] == 'alertStateChange':
                alh = AlertHandler(message)
                return alh.routing()
            elif message["data"]["objectType"] == 'assessmentStateChange':
                ash = AssessmentHandler(message)
                return ash.routing()
            else:
                return 'Bad Request', 400
        else:
            return 'Method Not Allowed', 405

    return app