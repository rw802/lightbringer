from googlevoice import Voice
from googlevoice.util import input

class GoogleVoice:
    def __init__(self, email, password):
        self.handle = Voice()
        self.handle.login(email, password)
        
    def send(self, dstNumber, msg):
        self.handle.send_sms(dstNumber, msg)
        