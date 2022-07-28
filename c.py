import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.43.73", 25561))

while True:
    client_socket.send("Ok")
    data = client_socket.recvfrom(20)
    print(data)
