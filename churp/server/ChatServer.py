#!/usr/local/bin/python3

'''
Author: RWC
Last Updated: 003/03/2018
Purpose: This script will create a server to listen on a specific port;
       it will also return the the message received to the sender port
'''
#socket used to create connections
from socket import *
#datetime used to add a date for history of chat
from datetime import datetime
#base64 used to encode and decode data into readable and unreadable language
import base64
#random used to have python choose from a random list of strings
import random

#IP from command prompt by issuing the command 'ipconfig'
serverIP = gethostname()
serverPort = 12001
dataLen = 1000000

# Create a UDP socket using IPv4
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
    userJoinMSG = ''

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
    #data=rawData.decode()
    data = base64.b64decode(rawData).decode('utf-8')
    print(data)

    #verifying protocols, a protocol of "1:" is client joining with specific username
    if data[0:2]== "1:":
        userName = data[2:]
        userInfo[userName]=address
        print(userInfo)
        #messages that are provided for new users that enter the chat
        introductions=[
                'has joined the chat!',
                'has ascended from the darkness',
                'spontaneously materialized',
                'just hacked into the chat',
                'is lurking nearby. Watch out',
                'heroically fought their way into our chat',
                'finally decided to show up',
                'just slid their way into our DMs ( ͡° ͜ʖ ͡°)',
                'crash landed into our chat',
                'is trying to make first contact',
                'just saw an alien or something and seriously needs to talk about it',
                'finally got their mom\'s permission to join our chat',
                'crawled fifteen miles to the nearest computer to join our chat'
        ]
        
        DefaultColor='#1b39c1'
        #The message that introduces new users to the server, using "introductions" list           
        userJoinMSG = "~~~ " + userName + " " + introductions[random.randint(0,len(introductions)-1)] + " " + "~~~" + DefaultColor
        for users in userInfo:
            serverSocket.sendto(base64.b64encode(userJoinMSG.encode('utf-8')),userInfo[users])
    #verifying protocols, a protocol of "2:" is client sending a message
    elif data[0:2]== "2:":
        message = data[2:]
        for users in userInfo:
            serverSocket.sendto(base64.b64encode(message.encode('utf-8')),userInfo[users])

        #creating a string concatenation of the message and time.
        historyMSG = currentTime + " => " + message[:-7] + "\n\n"
        
        try:
            #the message will be appended to the file that was declared.
            fileObject.write(historyMSG)
        except UnicodeEncodeError:
            pass
    elif data[0:2]=="3:":
        userName = data[2:]
        DefaultColor='#1b39c1'
        resignations=[
            'managed to escape our chatting prison',
            'hates us, especially you. They\'re out of here.',
            '? We out?',
            'dove out of a five story building to leave our chat',
            'needs to do their laundry because their mom told them to',
            'decided they were done talking to us',
            'dug their way out of our chat using a plastic spoon',
            'deconstructed themself atom by atom until they disappeared from our chat',
            'went into hyperdrive and is now 7 lightyears away from our chat'


        ]

        userLeaveMSG = "~~~ " + userName + " " + resignations[random.randint(0,len(resignations)-1)] + " " + "~~~" + DefaultColor
        #remove user from dictionary
        del userInfo[userName]
        
        #send msg that user left
        for users in userInfo:
            serverSocket.sendto(base64.b64encode(userLeaveMSG.encode('utf-8')),userInfo[users])

        
    fileObject.close()
    #END of While Loop
    
serverSocket.close()
