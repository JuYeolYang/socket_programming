import socket
import threading

HOST = 'localhost'
PORT = 9999

def receive():
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode())
        except:
            print("Connection closed")
            client_socket.close()
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Connected to server")

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    while True:
        message = input()
        if message == "/quit":
            break
        client_socket.sendall(message.encode())