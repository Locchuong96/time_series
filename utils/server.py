import socket

# IPV4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))

# Server listen 5 client
s.listen(5) # repair for connection, queue=5


while True:
    # Accept client
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    # Send message for client
    clientsocket.send(bytes("Welcome to the server!","utf-8")) # send information to client
    
    