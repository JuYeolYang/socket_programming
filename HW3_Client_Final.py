import socket

# 서버 정보
SERVER_HOST = '172.31.39.218'
SERVER_PORT = 8000

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print('DNS 서버에 연결되었습니다.')

while True:
    # 사용자 입력 받기
    request = input('요청을 입력하세요 ("DISCONNECT"로 연결 종료): ')

    # 서버로 요청 전송
    client_socket.sendall(request.encode())

    # 연결 종료 요청인 경우 루프 종료
    if request == 'DISCONNECT':
        break

    # 서버로부터 응답 수신
    response = client_socket.recv(1024).decode()

    # 응답 출력
    print('서버 응답:', response)

# 클라이언트 소켓 연결 종료
client_socket.close()
