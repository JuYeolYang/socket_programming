import socket
from _thread import *

HOST = 'localhost'
PORT = 50000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print ('>> Connect Server')

while True:
    message = input('보낼 문자를 입력하세요: ')
    if message == 'quit':
        close_data = message
        break
    client_socket.sendall(message.encode())
    print('Sended:', message)

    data = client_socket.recv(1024)
    print('Received ', data.decode())

client_socket.close()