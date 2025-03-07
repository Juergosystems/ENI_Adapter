class Config:

    class App:
            SECRET_KEY = 'qwertyuioplkmjnha5526735gbsgs'

    class Alert:
        class State:
            MONITORING = 0
            OPEN = 1
            CLOSED = 2
            REOPEN = 3

        class Status:
            AWAITING_ALLOCATIN = 100
            UNDER_INVESTIGATION = 101
            COMPLIANCE_CHECK = 102
            ESCALATED = 103
            FOUR_EYES_CHECK = 109
            REQUEST_TO_CLOSE = 195
            CLOSED_WITH_ACTION = 200
            CLOSED_WITHOUT_ACTION = 201
            REOPENED = 300

    class Assessment:
        class State:
            MONITORING = 0
            OPEN = 1
            CLOSED = 2

        class Status:
            AWAITING_ALLOCATIN = 100
            UNDER_INVESTIGATION = 101
            COMPLIANCE_CHECK = 102
            ESCALATED = 103
            FOUR_EYES_CHECK = 109
            WAIT_TO_CLOSE = 199
            CLOSED = 200
