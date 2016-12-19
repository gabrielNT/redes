class Message:
    """Class for messages"""
    def __init__(self, receiver, sender, message):
        self._receiver = receiver
        self._sender = sender
        self._message = message

    def getReceiver(self):
        return self._receiver

    def setReceiver(self, receiver):
        self._receiver = receiver

    def setSender(self, sender):
        self._sender = sender

    def getSender(self):
        return self._sender

    def getMessage(self):
        return self._message

    def setMessage(self, message):
        self._message = message

    receiver = property(getReceiver, setReceiver)
    sender = property(getSender, setSender)
    message = property(getMessage, setMessage)