import sys
import socket
import select
import threading
import cPickle as pickle
import json
from message import Message

RCV_BUFFER_SIZE = 4096
CLIENT_RECEIVER = "NOT085NOME"

class Client:
    def __init__(self):
        self.username = ""
        self.msg_list = []
        self.rcv_list = []
        self.user_list = []

    def start(self, host_address, port, username):
        self.username = username

        # Create the socket as an IFNET, with a data stream
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(4)

        # Connect to the server and send the user data
        try:
            client_socket.connect((host_address, port))
            client_socket.send(username)
        except:
            print 'Unable to establish connection'
            sys.exit()

        # Uses separate threads to check if needs to send or receive messages
        readable_fd = []
        threading.Thread(target=send_msg_thread, args=[client_socket, username, self]).start()
        threading.Thread(target=recv_msg_thread, args=[client_socket, self]).start()

    def send_message(self, receiver, message):
        new_message = Message(receiver, self.username, message)
        self.msg_list.append(new_message)

    def request_user_list(self):
        send_message(CLIENT_RECEIVER, 0)

    def getRcvList(self):
        return self.rcv_list

    def setRcvList(self, rcv_list):
        self.rcv_list = rcv_list

    rcv_list = property(getRcvList, setRcvList)

def send_msg_thread(sock, username, client):
        while True:
            if len(client.msg_list):
                for msg in client.msg_list:
                    print "Sending message " + msg.message
                    serial_msg = pickle.dumps(msg, -1)
                    sock.send(serial_msg)
                    client.msg_list.remove(msg)

def recv_msg_thread(sock, client):
        while True:
            read_list, _, _ = select.select([sock], [], [])
            for read_item in read_list:
                data = sock.recv(RCV_BUFFER_SIZE)
                print "Receiving Message"
                if data:
                    client.rcv_list.append(data)
                else:
                    print 'Disconnected from the server'
                    sys.exit()
