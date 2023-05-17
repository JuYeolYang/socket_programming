import socket

host = '127.0.0.1'
port = 20000
addr = (host, port)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_sock.connect(addr)
except Exception as e:
    print("error: ", e)

#메세지 내용
msg_list = ["I:1.1.1.1",
            "D:test1.com",
            "W:test3.com(3.3.3.3)"]

#메세지 전송
for msg in msg_list:
    client_sock.sendall(msg.encode('utf-8'))
    data = client_sock.recv(1024).decode('utf-8')
    print("recv: \n", repr(data))

#소켓 닫기
client_sock.close()