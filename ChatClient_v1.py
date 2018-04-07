from sys import exit
from tkinter import *
from tkinter.colorchooser import *
from threading import Thread
from socket import *
import base64

color = "#000000"
bgColor = "#4dffff"
dataLen = 1000000

serverIP = '128.235.217.98'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)

#listens for messages
def listener():
	while(True):
		rawData, address = clientSocket.recvfrom(dataLen)
		#data=rawData.decode()
		data = base64.b64decode(rawData).decode('utf-8')
		message = data[:-7]
		textColor = data[-7:]
		listBox.insert(END, message)
		listBox.itemconfig(END, {'fg': textColor})
		listBox.see(END)
		
#sends messages
def chatter():
	print("world")

def connect(event = None):
	if username.get().strip():
		messageProtocol = "1:" + username.get()
		clientSocket.sendto(base64.b64encode(messageProtocol.encode('utf-8')), (serverIP, serverPort))
		signIn.destroy()
		
def close():
	exit(0)
	
def send(event=None):
	global color
	if message.get().strip():
		messageProtocol = "2:" + username.get() + ": " + message.get() + color
		clientSocket.sendto(base64.b64encode(messageProtocol.encode('utf-8')), (serverIP, serverPort))
		message.set("")
		messageEntry.focus()
		
        
def changeColor(event=None):
	global color
	color = askcolor()
	color = color[1]
	colorButton.config(bg = color)
	messageEntry.config(foreground = color)
	userLabel.config(foreground = color)
	messageEntry.focus()
	
def changeBackground(event=None):
	global bgColor
	bgColor = askcolor()
	bgColor = bgColor[1]
	chatBox.config(bg = bgColor)
	botFrame.config(bg = bgColor)
	userLabel.config(bg = bgColor)

if __name__ == "__main__":
	#login
	signIn = Tk()
	signIn.title("RWC Login")
	signIn.protocol("WM_DELETE_WINDOW", close)
	
	userLabel = Label(signIn, text = "Enter your username:  ")
	userLabel.grid(row=0, column=0)
	
	username = StringVar()
	userEntry = Entry(signIn, textvariable=username)
	userEntry.grid(row=0,column=1)
	
	userEntry.bind("<Return>", connect)
	
	enterButton = Button(signIn, text="Sign In", command=connect)
	enterButton.grid(row=0, column=2)
	
	userEntry.focus()
	signIn.mainloop()
	
	#create chat box
	
	#start multi-thread
	threadListener = Thread(target = listener)
	threadChatter = Thread(target = chatter)
	
	chatBox = Tk()
	chatBox["bg"] = bgColor
	chatBox.title("RWC Chat")
	chatBox.protocol("WM_DELETE_WINDOW", close)

	#menubar
	menubar = Menu(chatBox)

	fileMenu = Menu(menubar, tearoff=0)
	fileMenu.add_command(label="Exit", command=close)
	menubar.add_cascade(label="File", menu=fileMenu)
        
	editMenu = Menu(menubar, tearoff=0)
	editMenu.add_command(label="Change Background Color", command=changeBackground)
	menubar.add_cascade(label="Edit", menu=editMenu)

	chatBox.config(menu=menubar)

	message = StringVar()
        #top frame
	topFrame = Frame(chatBox)
	topFrame.pack(fill=BOTH, expand=True, padx = 20, pady = 20)
	scrollBar = Scrollbar(topFrame, orient=VERTICAL)
	scrollBar.pack(side=RIGHT, fill=Y)
	listBox = Listbox(topFrame, yscrollcommand=scrollBar.set)
	listBox.pack(side=LEFT, expand=True, fill=BOTH)
	scrollBar.config(command=listBox.yview)
        #bot frame
	botFrame = Frame(chatBox, height = 1, bg = bgColor)
	botFrame.pack(fill=X, padx = 20)
	userLabel = Label(botFrame, text = "%s: " % username.get(), foreground=color, bg = bgColor)
	userLabel.pack(side=LEFT)
	
	messageEntry = Entry(botFrame, textvariable=message, foreground=color)
	messageEntry.bind("<Return>", send)

	sendButton = Button(botFrame, text="Send", command=send)
	sendButton.pack(side=RIGHT)

	colorButton = Button(botFrame, text=" ", command=changeColor, bg=color, width = 3)
	colorButton.pack(side=RIGHT, padx = 10)
	messageEntry.pack(expand=True, fill=BOTH)
		#spacer
	spacerFrame = Frame(chatBox)
	spacerFrame.pack(pady = 10)

	chatBox.iconbitmap(r'C:\Users\ps592\ChatApp\ChatAppinProgress')
	
	threadListener.start()
	threadChatter.start()
	
	chatBox.mainloop()
