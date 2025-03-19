from flask import current_app as app
from flask import request, jsonify
from config import Config as cfg


class AlertHandler:
    def __init__(self, message):
        self.message_id = message["id"]
        self.message_time = message["time"]["delivered"]
        self.message_type = message["type"]
        
        self.alert_id = message["data"]["objectId"]

        self.alert_before = message["data"]["objectBefore"]
        if self.alert_before is not None:
            self.state_before = message["data"]["objectBefore"]["state"]
            self.score_before = message["data"]["objectBefore"]["score"]
            self.docCount_before = message["data"]["objectBefore"]["docCount"]
            self.securityTag_before = message["data"]["objectBefore"]["security"]["orTags1"][0] if message["data"]["objectBefore"]["security"]["orTags1"] else None
            self.assignee_before = message["data"]["objectBefore"]["assignedUsers"][0]["id"] if message["data"]["objectBefore"]["assignedUsers"] else None
            self.status_before = message["data"]["objectBefore"]["currentStatus"]["code"]
        
        self.alert_after = message["data"]["objectAfter"]
        if self.alert_after is not None:
            self.state_after = message["data"]["objectAfter"]["state"]
            self.score_after = message["data"]["objectAfter"]["score"]
            self.docCount_after = message["data"]["objectAfter"]["docCount"]
            self.securityTag_after = message["data"]["objectAfter"]["security"]["orTags1"][0] if message["data"]["objectAfter"]["security"]["orTags1"] else None
            self.assignee_after = message["data"]["objectAfter"]["assignedUsers"][0]["id"] if message["data"]["objectAfter"]["assignedUsers"] else None
            self.status_after = message["data"]["objectAfter"]["currentStatus"]["code"]

    def routing(self):
        if self.alert_before is None:
            self.new_alert()
        
        info = "Message successfully processed"
        response = jsonify({"message_id":self.message_id, "status": info})
        app.logger.info(response)
        return response, 200

    def new_alert(self):
        if self.state_after == cfg.Alert.State.OPEN:
            return
        return
    
    def updated_alert(self):
        return
    
    def closed_alert(self):
        return
    
    def reopened_alert(self):
        return



