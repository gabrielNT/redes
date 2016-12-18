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
CLIENT_RECEIVER = "NOT085NOME"

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
                    # TODO: Check if name already exists
                    username = new_socket.recv(RCV_BUFFER_SIZE)
                    # Create a new user and put the data in the lists
                    new_user = User(username, new_socket)
                    self.user_list.append(new_user)
                    SOCKET_LIST.append(new_socket)
                    print "User " + new_user.name + " on (%s, %s) connected" % new_socket_address

                else:
                   try:
                        serial_msg = sock.recv(RCV_BUFFER_SIZE)
                        if serial_msg:
                            msg = pickle.loads(serial_msg)
                            if msg.receiver ==
                            self.cast(msg)
                        else:
                            # TODO: Check what else to remove
                            #if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                            for user_to_delete in self.user_list:
                                if sock == user_to_delete.socket:
                                    self.user_list.remove(user_to_delete)
                                    print "User " + user_to_delete.name + " disconnected"
                   except:
                       continue

    def cast(self, msg):
        receiver_counter = 0

        for receiver in msg.receiver:
            for user in self.user_list:
                if receiver == user.name:
                    receiver_counter += 1
                    try:
                        print "Sending message"
                        user.socket.send(msg.message)
                    except:
                        # The connection should be broken
                        user.socket.close()
                        SOCKET_LIST.remove(user.socket)
                        self.user_list.remove(user)
                        print "User " + user.name + " disconnected"

        if receiver_counter != len(msg.receiver):
            print "Only " + str(receiver_counter) + " of " + str(len(msg.receiver)) + "was found"

    def getUserList(self):
        return self.user_list

    def setUserList(self, user_list):
        self.user_list = user_list

    user_list = property(getUserList, setUserList)

if __name__ == "__main__":
    server = Server()
    sys.exit(server.messenger_server())
