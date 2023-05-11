import socket

host = '127.0.0.1'
port = 20000
addr = (host, port)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_sock.connect(addr)
except Exception as e:
    print("error: ", e)

msg = "I:1.1.1.1"
client_sock.sendall(msg.encode('utf-8'))
data = client_sock.recv(1024)
print("recv: \n", repr(data.decode('utf-8')))

msg = "D:test1.com"
client_sock.sendall(msg.encode('utf-8'))
data = client_sock.recv(1024)
print("recv: \n", data.decode('utf-8'))

client_sock.close()