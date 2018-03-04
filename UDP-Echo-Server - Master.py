#!/usr/local/bin/python3

'''
Author: RWC
Last Updated: 003/03/2018
Purpose: This script will create a server to listen on a specific port;
       it will also return the the message received to the sender port
'''

from socket import *
from datetime import datetime

#IP from command prompt by issuing the command 'ipconfig'
serverIP = '127.0.0.1' 
serverPort = 12001
dataLen = 1000000

# Create a UDP socket.
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
print('The server is ready to serve on port: ' + str(serverPort))

userInfo={}

# loop forever listening for incoming datagram messages
while True:
    #initializing variables
    historyMSG=''
    rawData = ''
    address= ''

    #Exception handling, errors are encountered when clients try to reset their connection
    try:
        rawData, address = serverSocket.recvfrom(dataLen)
        #Getting time of when the message was received in.
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #creating a text file to store messages received in
        fileObject=open('ChatHistory.txt', 'a')
    except ConnectionResetError:
        continue #we continue because if there is an error, we want to restart the while loop from top

    #converting network byte format into ascii string format
    data=rawData.decode()
    print(data)

    #verifying protocols, a protocol of "1:" is client joining with specific username
    if data[0:2]== "1:":
        userName = data[2:]
        userInfo[userName]=address
        print(userInfo)
    #verifying protocols, a protocol of "2:" is client sending a message
    elif data[0:2]== "2:":
        message = data[2:]
        for users in userInfo:
            serverSocket.sendto(message.encode(),userInfo[users])
        #creating a string concatenation of the message and time.
        historyMSG = currentTime + " => " + message + "\n\n"
        #the message will be appended to the file that was declared.
        fileObject.write(historyMSG)
        
    fileObject.close()
    #END of While Loop
    
serverSocket.close()
