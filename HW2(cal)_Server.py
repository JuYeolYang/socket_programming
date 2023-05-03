import socket

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server is listening on port {PORT}...')

    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')

        while True:
            data = conn.recv(1024)
            if not data:
                break

            expr = data.decode()
            try:
                result = eval(expr)
                conn.sendall(str(result).encode())
            except:
                conn.sendall(b'Input Error')