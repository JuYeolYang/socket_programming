#import socket for socket programming
from socket import *
#import os to get path of current directory
import os

#prepare server socekt - TCP
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12345
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print('Ready to serve...')
#create connection socket
connectionSocket, addr = serverSocket.accept()
#get path of current directory
#execute server.py program on problem8 directory -> current_dir = HW2_2017310301/problem8
current_dir = os.getcwd()
#open sent_data.txt file stored in HW2_2017310301/problem8/server and read the file as binary
f = open(current_dir + '/sent_data.txt', 'rb')
try:
    #save the data read from the sent_data.txt file
    data = f.read(1024)
    #send data through connectino socket
    connectionSocket.send(data.encode())
#handle exception
except Exception:
    print(Exception)
#close socket
serverSocket.close()