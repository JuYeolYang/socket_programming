import socket
from SOLVE import received_data_processing

host = '172.30.1.14' #변경필요
port = 8000

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((host, port))
server_sock.listen()

client_sock, addr = server_sock.accept()

print("client addr: ", addr)

while True:
    data = client_sock.recv(1024)
    # 빈 문자열을 수신하면 루프를 중지합니다.
    if not data:
        break

    decode_data = data.decode('utf-8')
    # 수신받은 문자열을 출력합니다.
    print('Received from', addr, decode_data)
    send_data = received_data_processing(decode_data)
    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코)
    client_sock.sendall(send_data.encode('utf-8'))

# 소켓을 닫습니다.
client_sock.close()
server_sock.close()
