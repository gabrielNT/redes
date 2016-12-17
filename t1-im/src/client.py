import sys
import socket
import select
from user import User

def messenger_client():
    if (len(sys.argv) < 4):
        print 'Instructions : python chat_client.py hostname port username'
        sys.exit()

    # Uses command-line arguments for the parameters
    host_address = sys.argv[1]
    port = int(sys.argv[2])
    username = str(sys.argv[3])

    # Create the socket as an IFNET, with a data stream
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(4)

    try:
        client_socket.connect((host_address, port))
        client_socket.send(username)
    except:
        print 'Unable to establish connection'
        sys.exit()

    while True:
        # We have to process something either when the socket needs to read something or
        # the user wants to write
        file_descriptors_list = [sys.stdin, client_socket]
        # This time we want to block the operation hear, waiting for a readable fd
        readable_fd, writeable_fd, error_fd = select.select(file_descriptors_list, [], [])

if __name__ == "__main__":
    sys.exit(messenger_client())