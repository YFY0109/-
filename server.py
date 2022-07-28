import socket
import threading

from imgscan import *


PORT = 25561
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.202.182", PORT) #! 
server_socket.bind(address)
server_socket.settimeout(5)
client, ctemp = None, []


def start():
    global client
    while True:
        try:
            receive_data, client = server_socket.recvfrom(20)
            if client != ctemp:
                print("Info: Get controler from %s" % str(client))
                ctemp.append(client)
            # if len(ctemp) > 1:
            #     print("Warning: Controlers is more than 1.")
            if receive_data == "shutdown":
                break
            if len(result) > 0:
                server_socket.sendto(f"{result[-1]}, {len(result)}", client)
        except socket.timeout:
            if client is None:
                print("Error: Timed out!")
    print("Server closed")


server_thread = threading.Thread(target=start)

if __name__ == "__main__":
    server_thread.start()
    detect()
