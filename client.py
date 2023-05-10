import socket
import time

# 서버 설정
HOST = 'localhost'
PORT = 8000

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    # 사용자 입력 받기
    request = input('요청을 입력하세요(function domain ip)\n')

    # 요청 전송
    client_socket.sendall(request.encode())

    # 응답 수신
    time.sleep(0.1)
    response = client_socket.recv(1024).decode()

    # 응답 출력
    print('서버 응답:', response)

    # 도메인 검색인 경우, IP 주소 출력
    if response.startswith('해당 도메인이 존재합니다.'):
        _, ip_address = response.split(':')
        print('IP 주소:', ip_address)

    # 종료 조건
    if request == 'EXIT':
        break

# 소켓 연결 종료
client_socket.close()
