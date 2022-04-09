#<---------------------------MODULES-------------------------------->
from tkinter import *
import socket
import threading
import time
#<-------------------------CONSTANTS-------------------------------->
# Server Port Number : 5050
PORT = 5050

# Server Address : localhost(Within the Device) and can be changed to any IPv4 address
SERVER = "localhost"

# Address : (SERVER, PORT) tuple
ADDR = (SERVER, PORT)

# Format : "utf-8" used for encoding and decoding
FORMAT = "utf-8"

# Message to Disconnect to server
DISCONNECT_MESSAGE = "!DISCONNECT"

# All time zones available for the client to check date and time
Country_Zones = ['America/New_York', 'Asia/Kolkata', 'Australia/Sydney', 'Canada/Atlantic', 'Brazil/East','Chile/EasterIsland', 'Cuba', 'Egypt','Europe/Amsterdam', 'Europe/Athens', 'Europe/Berlin', 'Europe/Istanbul','Europe/Jersey', 'Europe/London', 'Europe/Moscow', 'Europe/Paris', 'Europe/Rome', 'Hongkong', 'Iceland', 'Indian/Maldives', 'Iran','Israel', 'Japan', 'NZ', 'US/Alaska', 'US/Arizona', 'US/Central', 'US/East-Indiana']

#<-----------------MAIN----------------->

# AF_INET = Address Family IPv4
# SOCK_STREAM = TCP Connection
# socket -> Creates a socket for client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    """Function which establishes a connection to the server"""
    client.connect(ADDR)
    return client

def disconnect():
    """Function which disconnects from the server by sending an DISCONNECT message and closes the application"""
    send(connection, DISCONNECT_MESSAGE)
    client.close()
    root.destroy()
    quit()

def send(client, msg):
    """Function which sends the message to the server from the client requesting for the date and time of the requested zone"""
    message = msg.encode(FORMAT)
    client.send(message)

def recieve():
    """Function which recieve and displays date and time from the server without any packet loss"""
    message = client.recv(1024).decode(FORMAT)
    if not message:
        print("Disconnected")
        return
    else:
        Time_Label.config(text = f"Zone : {clicked.get()} {message}")
    
def start1():
    global t1
    t1 = threading.Thread(target = start)
    t1.start()

def start():
    """Requests for the time zone to the server"""
    while 1:
        send(connection, clicked.get())
        recieve()
        time.sleep(1)


def GUI():
    """Function which creates Graphical User Interface for the Client to communicate to the server"""
    global Time_Label, clicked, root
    root = Tk()
    root.title("Client - Time Receiver")
    root.geometry("500x250")
    root.resizable(0,0)
    root.configure(bg="#2d0365")

    heading_label = Label(root, text="Time Receiver", font=("Cascadia Code", 20), bg = "#2d0365", fg = "yellow")	
    heading_label.grid(row=0, column=0, columnspan=3)

    About_label = Label(root, bg = "#2d0365", fg = "yellow", text=" This is a Client side application which connects to the time\n server using TCP connection, and then recieves the Time from\nthe server and displays to the user.", font=("Cascadia Code", 10))
    About_label.grid(row=1, column=0, columnspan=3)

    Label(root, text="Enter the Zone to get the Time :", font=("Cascadia Code", 10), bg = "#2d0365", fg = "yellow").grid(row=2, column=1)

    clicked = StringVar()
    clicked.set(Country_Zones[0])

    drop = OptionMenu(root, clicked, *Country_Zones)
    drop.configure(bg = "#00FFFF", fg = "black", font=("Cascadia Code", 10))
    drop.grid(row=3, column=1, pady=5)

    start1()
    Button(root, bg = "red", fg = "white", text = "Close Application", command = disconnect, font=("Cascadia Code", 10)).grid(row=6, column=1, pady=5)

    Time_Label = Label(root, text="", font=("Cascadia Code", 10), bg = "#2d0365", fg = "yellow")
    Time_Label.grid(row=5, column=1,pady=5)
    root.mainloop()

# Starts the connection
connection = connect()

# GUI function Call
GUI()

#<---------------------END OF THE CLIENT SIDE PROGRAM------------------->
# Developed by : Hari Om Swarup S A
# PESU EC Campus