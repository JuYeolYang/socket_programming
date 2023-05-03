import socket

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f'Connected to server {HOST}:{PORT}')

    while True:
        expr = input('Enter an expression (q to quit): ')
        if expr == 'q':
            break

        s.sendall(expr.encode())
        data = s.recv(1024)

        print(data.decode())