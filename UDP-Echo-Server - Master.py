#!/usr/local/bin/python3

# Author: Mickey Somra
# Last Updated: 01/24/2018
# Purpose: This script will create a server to listen on a specific port;
#       it will also return the the message received to the sender port

from socket import *
serverIP = '128.235.217.98' # any local IP address
serverPort = 12001
dataLen = 1000000

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
print('The server is ready to receive on port: ' + str(serverPort))

userInfo={}

# loop forever listening for incoming datagram messages
while True:
    rawData = ''
    address= ''
    # Receive and print the client data from "data" socket
    try:
        rawData, address = serverSocket.recvfrom(dataLen)
    except ConnectionResetError:
        pass
    
    data=rawData.decode()
    print(data)
    
    if data[0:2]== "1:":
        userName = data[2:]
        userInfo[userName]=address
        print(userInfo)
    elif data[0:2]== "2:":
        message = data[2:]
        print(message)
        for users in userInfo:
            serverSocket.sendto(message.encode(),userInfo[users])

