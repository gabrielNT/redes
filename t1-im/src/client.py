import sys
import socket
import select
import threading
import cPickle as pickle
from message import Message

RCV_BUFFER_SIZE = 4096

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
            code = client_socket.recv(RCV_BUFFER_SIZE)
            if code == "2":
                print 'Username not alphanumeric'
                sys.exit()
            elif code == "3":
                print 'Username already in use'
                sys.exit()
            elif code == "4":
                sys.exit()
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

    def getRcvList(self):
        return self.rcv_list

    def setRcvList(self, rcv_list):
        self.rcv_list = rcv_list

    def getUserList(self):
        return self.user_list

    def setUserList(self, user_list):
        self.user_list = user_list

    user_list = property(getUserList, setUserList)
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

                data = read_item.recv(RCV_BUFFER_SIZE)
                if data:
                    # Operation 0 = send message
                    if data[0] == '0':
                        print "Receiving Message " + data[1:]
                        client.rcv_list.append(data[1:])
                    # Operation 1 = update user_list
                    elif data[0] == '1':
                        #print "Receiving user_list"
                        client.user_list = []
                        temp_string = data[1:]
                        client.user_list = temp_string.split(",")
                    else:
                        print "Operation not recognized."
                        continue
                else:
                    print 'Disconnected from the server'
                    sys.exit()