import socket

# Init client socket
s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server with specific port
s.connect((socket.gethostname(),1234))

# Get message lenght 1024 buffer from server
msg = s.recv(1024)

# Display message
print(msg.decode('utf-8'))