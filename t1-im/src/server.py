import sys
import socket
import select
import cPickle as pickle
from user import User
from message import Message

HOST_ADDRESS = ''
PORT = 8003
RCV_BUFFER_SIZE = 4096
SOCKET_LIST = []

class Server:
    def __init__(self):
        self.user_list = []

    def messenger_server(self):
        # Initialize the socket as an INET socket using data streams
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # To avoid problems with repeated addresses
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket and wait for connections
        server_socket.bind((HOST_ADDRESS, PORT))
        server_socket.listen(5)  # 5 sockets in queue should be enough

        SOCKET_LIST.append(server_socket)
        print "Server started on address " + str(HOST_ADDRESS) + "and port " + str(PORT)

        while True:
            # Uses the Unix call to select, checking which sockets are ready to be read, written or have pending conditions
            # The timeout argument is 0, so the operation is non-blocking
            readable_sockets, writeable_sockets, error_sockets = select.select(SOCKET_LIST, [], [], 0)

            for sock in readable_sockets:
                # If the readable socket is the server_socket itself, it must be trying to
                # open a new connection
                if sock == server_socket:
                    new_socket, new_socket_address = server_socket.accept()
                    self.broadcast_user_list(server_socket)
                    username = new_socket.recv(RCV_BUFFER_SIZE)

                    # Check if username is valid
                    if self.check_username(username) == 1:
                        # Create a new user and put the data in the lists
                        new_user = User(username, new_socket)
                        self.user_list.append(new_user)
                        SOCKET_LIST.append(new_socket)
                        print "User " + new_user.name + " on (%s, %s) connected" % new_socket_address
                        self.broadcast_user_list(server_socket)
                    else:
                        if self.check_username(username) == 0:
                            print "Username not alphanumeric " + username
                            new_socket.send("2")
                        else:
                            print "Username already in use: " + username
                            new_socket.send("3")
                        new_socket.close()
                else:
                   try:
                        serial_msg = sock.recv(RCV_BUFFER_SIZE)
                        if serial_msg:
                            msg = pickle.loads(serial_msg)
                            self.cast(msg, server_socket)
                        else:
                            sock.close()
                            SOCKET_LIST.remove(sock)
                            for user_to_delete in self.user_list:
                                if sock == user_to_delete.socket:
                                    self.user_list.remove(user_to_delete)
                                    print "User " + user_to_delete.name + " disconnected"
                            self.broadcast_user_list(server_socket)
                   except:
                       continue

    def cast(self, msg, server_socket):
        receiver_counter = 0

        for receiver in msg.receiver:
            for user in self.user_list:
                if receiver == user.name:
                    receiver_counter += 1
                    try:
                        data = "0[" + msg.sender + "]" + msg.message
                        print "Sending message " + data
                        user.socket.send(data)
                    except:
                        # The connection should be broken
                        user.socket.close()
                        SOCKET_LIST.remove(user.socket)
                        self.user_list.remove(user)
                        print "User " + user.name + " disconnected"
                        self.broadcast_user_list(server_socket)

        if receiver_counter != len(msg.receiver):
            print "Only " + str(receiver_counter) + " of " + str(len(msg.receiver)) + "was found"

    # Broadcast user_list to all clients
    def broadcast_user_list(self, server_socket):
        names = self.get_user_list_names()

        print "Sending user_list " + names
        for sock in SOCKET_LIST:
            if sock != server_socket:
                try:
                    sock.send(names)
                except:
                    # The connection should be broken
                    sock.close()
                    for user_to_delete in self.user_list:
                        if sock == user_to_delete.socket:
                            self.user_list.remove(user_to_delete)
                            print "User " + user_to_delete.name + " disconnected"
                    self.broadcast_user_list(server_socket)

    def check_username(self, username):
        # 0 if format is wrong, -1 if already exists, 1 if valid
        validity = 0
        if username.isalnum():
            validity = 1
            for user in self.user_list:
                if user.name == username:
                    validity = -1
                    break

        return validity

    def get_user_list_names(self):
        new_string = "1"
        for user in self.user_list:
            new_string += user.name
            new_string += ","
        return new_string

    def getUserList(self):
        return self.user_list

    def setUserList(self, user_list):
        self.user_list = user_list

    user_list = property(getUserList, setUserList)

if __name__ == "__main__":
    server = Server()
    sys.exit(server.messenger_server())
