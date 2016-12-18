import socket

class User:
    """Class for user data"""
    def __init__(self, name, socket):
        self._name = name
        self._socket = socket

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getSocket(self):
        return self._socket

    def setSocket(self, socket):
        self._socket = socket

    name = property(getName, setName)
    socket = property(getSocket, setSocket)
