class AssessmentHandler:
    def __init__(self, message):
        self.assessment_id = message["data"]["object"]["id"]
        self.assessment_before = message["data"]["objectBefore"]
        self.assessment_after = message["data"]["objectAfter"]
        self.message = message

    def routing(self):
        if self.assessment_before is None:
            return self.new_assessment()
        return

    def new_object(self):
        return
    
    def new_assignee(self):
        return
    
    def new_status(self):
        return
    
    def reopened(self):
        return

    def closed(self):
        return
    
    