import sys
import socket
import select
from user import User

HOST_ADDRESS = ''
PORT = 8003
RCV_BUFFER_SIZE = 4096
SOCKET_LIST = []
USER_LIST = []

def messenger_server():
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
                username = new_socket.recv(RCV_BUFFER_SIZE)
                SOCKET_LIST.append(new_socket)
                new_user = User(username, new_socket)
                USER_LIST.append(new_user)

                print "User " + new_user.name + " on (%s, %s) connected" % new_socket_address



if __name__ == "__main__":
    sys.exit(messenger_server())