# Client Side Chat Room
import socket, threading

# Define constants to be used
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

def send_message():
    ''' Send a message to the server to be broadcast'''
    pass


def receive_message():
    ''' Receive an incoming message from the server'''
    pass
