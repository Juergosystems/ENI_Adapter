from flask import current_app as app
from flask import request, jsonify
from config import Config as cfg

class AssessmentHandler:
    
    def __init__(self, message):
        self.message_id = message["id"]
        self.message_time = message["time"]["delivered"]
        self.message_type = message["type"]
        
        self.assessment_id = message["data"]["objectId"]

        self.assessment_before = message["data"]["objectBefore"]
        if self.assessment_before is not None:
            self.state_before = message["data"]["objectBefore"]["state"]
            self.owner_before = message["data"]["objectBefore"]["security"]["owners"][0] if message["data"]["objectBefore"]["security"]["owners"] else None
            self.assignee_before = message["data"]["objectBefore"]["entities"][0]["results"]["assignedUser"]["id"] if message["data"]["objectBefore"]["entities"][0]["results"] !={} else None
            self.status_before = message["data"]["objectBefore"]["entities"][0]["results"]["status"] if message["data"]["objectBefore"]["entities"][0]["results"] else None
        
        self.assessment_after = message["data"]["objectAfter"]
        if self.assessment_after is not None:
            self.state_after = message["data"]["objectAfter"]["state"]
            self.owner_after = message["data"]["objectAfter"]["security"]["owners"][0] if message["data"]["objectAfter"]["security"]["owners"] else None
            self.assignee_before = message["data"]["objectAfter"]["entities"][0]["results"]["assignedUser"]["id"] if message["data"]["objectAfter"]["entities"][0]["results"] != {} else None
            self.status_before = message["data"]["objectAfter"]["entities"][0]["results"]["status"] if message["data"]["objectAfter"]["entities"][0]["results"] else None

    def routing(self):
        if self.assessment_before is None:
            self.new_assessment()
        
        info = "Message successfully processed"
        response = jsonify({"message_id":self.message_id, "status": info})
        app.logger.info(response) 
        return response, 200

    def new_assessment(self):
        if self.state_after == cfg.Assessment.State.OPEN:
            return
        return
    
    def updated_assessment(self):
        return
    
    def closed_assessment(self):
        return
    
    
    