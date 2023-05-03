#import socket for socket programming
from socket import *
#import os to get path of current directory
import os
#import sys
import sys

#prepare client socket - TCP
serverName = '127.0.0.1'
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
#get path of current directory
#execute server.py program on problem8 directory -> current_dir = HW2_2017310301/problem8
current_dir = os.getcwd()
#create sent_data.txt file stored in HW2_2017310301/problem8/client and open to write in binary
f = open(current_dir + "/received_data.txt" , "wb")
try:
    #store data recieved from server througth client socket
    data = clientSocket.recv(1024)
    #write recieved data in new text file
    f.write(data)
    print(data)
#handle exception
except Exception:
    print(Exception)
#close socket
clientSocket.close()