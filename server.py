#<-----------------MODULES----------------->
import threading  # -> For multiprocessing
import socket  # -> Socket library
from datetime import datetime  # -> Date and time functions
import pytz  # -> Provides Date and time for different regions
#<---------------QUESTIONS----------------->
"""
### Questions?
1) Why TCP is used over UDP
Ans) UDP suffers from security issues. It is possible to spoof packets, causing clocks to set to various times (an issue for certain 
services that run periodically). There are several cases of misuse and abuse where server are the victims of DoS attacks
"""
#<---------------CONSTANTS----------------->
# Server Port Number : 5050
PORT = 5050

# Server Address : localhost(Within the Device) and can be changed to any IPv4 address
SERVER = "localhost"  # -> 127.0.0.1

# Address : (SERVER, PORT) tuple
ADDR = (SERVER, PORT)

# Format : "utf-8" used for encoding and decoding
FORMAT = "utf-8"

# Message to Disconnect to server
DISCONNECT_MESSAGE = "!DISCONNECT"

#<-----------------MAIN----------------->

# AF_INET = Address Family IPv4
# SOCK_STREAM = TCP Connection
# socket -> Creates a socket for server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Threading method is used to handle multiple clients at the same time(asynchronous)
clients = set()
clients_lock = threading.Lock()


def handle_client(conn, addr):
    """Function which handles the client request for the time zone"""
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data != DISCONNECT_MESSAGE:
            # print(f"Client {str(addr)} : Requested Time : {data}")
            country_time_zone = pytz.timezone(data)
            country_time = datetime.now(country_time_zone)
            timedata = country_time.strftime("Time : %H:%M:%S Date : %d-%m-%y")
            conn.send(timedata.encode())
        else:
            print(f"Client {str(addr)} : DISCONNECTED")
            break
    conn.close()


def start():
    """Function which starts the server"""
    print('[SERVER STARTED]')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        print(f"Client {str(addr)} : CONNECTED")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Starts the server side script
start()

#<-----------END OF THE SERVER SIDE PROGRAM---------------->
# Developed by : Hari Om Swarup S A
# PESU EC Campus