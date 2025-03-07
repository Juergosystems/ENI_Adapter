from config import Config as cfg

class AssessmentHandler:
    
    def __init__(self, message):
        self.message_id = message["id"]
        self.message_time = message["time"]["delivered"]
        self.message_type = message["type"]
        
        self.assessment_id = message["data"]["object"]["id"]

        self.assessment_before = message["data"]["objectBefore"]
        if self.assessment_before is not None:
            self.state_before = message["data"]["objectBefore"]["state"]
            self.score_before = message["data"]["objectBefore"]["score"]
            self.docCount_before = message["data"]["objectBefore"]["docCount"]
            self.owner_before = message["data"]["objectBefore"]["security"]["owners"][0]
            self.assignee_before = message["data"]["objectBefore"]["assignedUsers"][0]["id"]
            self.status_before = message["data"]["objectBefore"]["currentStatus"]["code"]
        
        self.assessment_after = message["data"]["objectAfter"]
        if self.assessment_after is not None:
            self.state_after = message["data"]["objectAfter"]["state"]
            self.score_after = message["data"]["objectAfter"]["score"]
            self.docCount_after = message["data"]["objectAfter"]["docCount"]
            self.owner_after = message["data"]["objectAfter"]["security"]["owners"][0]
            self.assignee_after = message["data"]["objectAfter"]["assignedUsers"][0]["id"]
            self.status_after = message["data"]["objectAfter"]["currentStatus"]["code"]

    def routing(self):
        if self.assessment_before is None:
            self.new_assessment()
        
        return {"id":self.message_id, "status": "Message successfully processed"}, 200

    def new_assessment(self):
        if self.state_after == cfg.Assessment.State.OPEN:
            return
        return
    
    def new_assignee(self):
        return
    
    def new_status(self):
        return
    
    def reopened(self):
        
        return

    def closed(self):
        return
    
    