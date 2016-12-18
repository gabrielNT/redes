import sys
import socket
import select
import threading
import cPickle as pickle
from message import Message

RCV_BUFFER_SIZE = 4096

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

    # Connect to the server and send the user data
    try:
        client_socket.connect((host_address, port))
        client_socket.send(username)
    except:
        print 'Unable to establish connection'
        sys.exit()

    if sys.platform.startswith('win32'):
        # sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        readable_fd = []
        threading.Thread(target=win32_send_msg_thread, args=[client_socket, username]).start()
        threading.Thread(target=win32_recv_msg_thread, args=[client_socket]).start()
    elif sys.platform.startswith('linux'):
        while True:
            # We have to process something either when the socket needs to read something or
            # the user wants to write
            # This time we want to block the operation hear, waiting for a readable fd
            file_descriptors_list = [sys.stdin, client_socket]
            readable_fd, _, _ = select.select(file_descriptors_list, [], [])

            for sock in readable_fd:
                # If the readable socket is the client itself, it should be receiving data from
                # the server.
                if sock == client_socket:
                    data = sock.recv(RCV_BUFFER_SIZE)
                    if data:
                        # TODO: Send in a way to connect to the front end
                        sys.stdout.write(data)
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()
                    else:
                        print 'Disconnected from the server'
                        sys.exit()
                # If not, then the readable fd is the user message
                else:
                    #TODO: Connect to front end
                    msg_body = sys.stdin.readline()
                    new_message = Message(['joao'], username, msg_body)
                    serial_msg = pickle.dumps(new_message, -1)
                    client_socket.send(serial_msg)

def win32_send_msg_thread(sock, username):
    while True:
        msg_body = sys.stdin.readline()
        new_message = Message(['joao'], username, msg_body)
        serial_msg = pickle.dumps(new_message, -1)
        sock.send(serial_msg)

def win32_recv_msg_thread(sock):
    while True:
        read_list, _, _ = select.select([sock], [], [])
        for read_item in read_list:
            data = sock.recv(RCV_BUFFER_SIZE)
            if data:
                # TODO: Send in a way to connect to the front end
                sys.stdout.write(data)
            else:
                print 'Disconnected from the server'
                sys.exit()

if __name__ == "__main__":
    sys.exit(messenger_client())