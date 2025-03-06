class AlertHandler:
    def __init__(self, message):
        self.message = message

    def routing(self):
        if self.message["data"]["objectBefore"] is None:
            return self.new_alert()
        return
    
    def new_alert(self):
        return




