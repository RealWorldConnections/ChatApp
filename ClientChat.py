from sys import exit

from sys import version_info

from datetime import datetime

from socket import *

from threading import Thread

serverIP = '128.235.217.98'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)

if version_info[0] == 2:

    from Tkinter import *

    from tkColorChooser import askcolor

elif version_info[0] == 3:

    from tkinter import *

    from tkinter.colorchooser import *

else:

    sys.exit(1)



def saveConfig(key):

    print("save config")



def applyChanges(key):

    print("apply changes")



def close():

    # deregister with the server

    # save settings

    exit(0)

def updateListBox():
    while True:
        print("Waiting to recv")
        recvMessage, address = clientSocket.recvfrom(65535)
        listBox.insert(END, recvMessage.decode())
        listBox.yview(END)
        print("is recv")

def connect(event=None):

    if username.get():

        #1: is for username requeset.
        usernameProtocol = "1:" + username.get()

        clientSocket.sendto(usernameProtocol.encode(), (serverIP, serverPort) )
        
        # send username to server

        # check to see if username taken already

        # if not destroy window forr username request

      
        user.destroy()



def send(event=None):

    message = strVar.get()

    strVar.set("")

    if message:

        messageProtocol = "2:" + username.get() + ": " + message

        clientSocket.sendto(messageProtocol.encode(), (serverIP, serverPort) )
        
        #listBox.insert(END, message)

        #listBox.yview(END)



def getColor():

    color = askcolor()



def time():

    time = Tk()

    time.title("Time")



    yearFrame = Frame(time)

    yearFrame.pack()

    yearLabel = Label(yearFrame, text="Year")

    yearLabel.pack()



    time.mainloop()



def colors():

    colors = Tk()

    colors.title("Colors")

    

    sendColorFrame = Frame(colors)

    sendColorFrame.pack()

    sendColorLabel = Label(sendColorFrame, text="Send Button")

    sendColorLabel.pack()

    sendColorButton = Button(sendColorFrame, command=getColor)

    sendColorButton.pack()



    textColorFrame = Frame(colors)

    textColorFrame.pack()

    textColorLabel = Label(sendColorFrame, text="Text")

    textColorLabel.pack()

    textColorButton = Button(textColorFrame, command=getColor)

    textColorButton.pack()



    chatBoxFrame = Frame(colors)

    chatBoxFrame.pack()

    chatBoxLabel = Label(chatBoxFrame, text="Chat Box")

    chatBoxLabel.pack()

    chatBoxButton = Button(chatBoxFrame, command=getColor)

    chatBoxButton.pack()



    saveButton = Button(colors, text="Save", command=saveConfig)

    saveButton.pack()



    applyButton = Button(colors, text="Apply", command=applyChanges)

    applyButton.pack()



    colors.mainloop()

    

def font():

    font = Tk()

    font.title("Font")



    typefaceFrame = Frame(font)

    typefaceFrame.pack()

    typefaceLabel = Label(typefaceFrame, text="Typeface")

    typefaceLabel.pack()



    fontSizeFrame = Frame(font)

    fontSizeFrame.pack()

    fontSizeLabel = Label(fontSizeFrame, text="Size")

    fontSizeLabel.pack()



    saveButton = Button(font, text="Save", command=saveConfig)

    saveButton.pack()



    applyButton = Button(font, text="Apply", command=applyChanges)

    applyButton.pack()



    font.mainloop()



# ask for the username

if __name__ == "__main__":

    user = Tk()

    user.title("RWC Chat App")

    user.protocol("WM_DELETE_WINDOW", close)



    username = StringVar()



    usernameLabel = Label(user, text="Enter your username. ")

    usernameLabel.grid(row=0, column=0)



    usernameEntry = Entry(user, textvariable=username)

    usernameEntry.grid(row=0, column=1)

    usernameEntry.bind("<Return>", connect)



    enterButton = Button(user, text="Welcome!", command=connect)

    enterButton.grid(row=0, column=2)



    user.mainloop()



    # open the chat app

    root = Tk()

    root.title("RWC Chat App")

    root.geometry("500x500")

    root.protocol("WM_DELETE_WINDOW", close)



    strVar = StringVar()



    menuBar = Menu(root)

    root.config(menu=menuBar)



    optionsMenu = Menu(menuBar, tearoff=0)

    optionsMenu.add_command(label="Fonts", command=font)

    optionsMenu.add_command(label="Colors", command=colors)

    optionsMenu.add_command(label="Time", command=time)

    menuBar.add_cascade(label="Options", menu=optionsMenu)



    botFrame = Frame(root, width=500)

    botFrame.pack(side=BOTTOM, fill=X)



    entry = Entry(botFrame, textvariable=strVar)

    entry.pack(side=LEFT, expand=True, fill=X)

    entry.bind("<Return>", send)



    sendButton = Button(botFrame, text="Send", command=send)

    sendButton.pack(side=RIGHT)



    topFrame = Frame(root)

    topFrame.pack(side=TOP, fill=BOTH, expand=True)

    scrollBar = Scrollbar(topFrame, orient=VERTICAL)

    scrollBar.pack(side=RIGHT, fill=Y)



    listBox = Listbox(topFrame, yscrollcommand=scrollBar.set)

    listBox.pack(side=LEFT, expand=True, fill=BOTH)

    
    scrollBar.config(command=listBox.yview)

    t1 = Thread(target = updateListBox)
    t1.start()
    
    root.mainloop()



    # load config files
