import socket
import time

host = '172.30.1.14'  # 서버의 IP 주소 변경필요!
port = 8000  # 서버의 포트 번호

connected = False
start_time = time.time()
while not connected:
    try:
        # 서버에 연결
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        connected = True
    except ConnectionRefusedError:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 10:
            print('서버에 연결할 수 없습니다. 대기 시간이 초과되었습니다.')
            break
        print('서버에 연결할 수 없습니다. 대기 모드로 전환합니다.')
        time.sleep(1)
print('서버에 연결되었습니다.')
while True:
    # 사용자로부터 입력 받기
    message = input('메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): ')

    if message.lower() == 'q':
        break

    # 메시지를 서버로 전송
    client_socket.sendall(message.encode('utf-8'))

    # 서버로부터 응답 받기
    data = client_socket.recv(1024)
    response = data.decode('utf-8')

    # 응답 출력
    print('서버 응답:', response)

# 소켓 닫기
client_socket.close()
