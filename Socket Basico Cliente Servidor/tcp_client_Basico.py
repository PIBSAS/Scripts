# TCP Client side

import socket

# Create a client side IPV4 socket (AF_INET) and TCP (SOCL_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to a server locate at a given IP and Port
client_socket.connect((socket.gethostbyname(socket.gethostname()), 12345))

# Receive a message from the server... You must specify the max of bytes to recieve
message = client_socket.recv(1024)
print(message.decode('utf-8'))

# Close the client socket
client_socket.close()
