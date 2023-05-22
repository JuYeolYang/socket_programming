import socket
import time
import math
import os

host = '192.168.18.1'
port = 20000
addr = (host, port)
connect = True
startTime = time.time()
while connect:
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(addr)
        connect = False # 서버와 연결됨
    except ConnectionRefusedError: #서버와 연결되지 않음
        endTime = time.time()
        overTime = endTime - startTime
        if overTime < 10: # 10초 동안 기다림
            os.system('clear')
            print("서버와 연결 중 입니다", "."*(math.floor(overTime) % 3 + 1))
            time.sleep(1)
        else:
            os.system('clear')
            print("서버 접속 시간이 지났습니다. 프로그램을 종료합니다")
            exit()
    except BrokenPipeError:
        print("서버와 연결할 수 없습니다")
        exit()
#메세지 전송
while True:
    msg = str(input("Input command(if you want to exit, enter 'exit' or ENTER): "))
    
    if msg == "exit" or msg == "\n":
        break
    client_sock.sendall(msg.encode('utf-8'))
    data = client_sock.recv(1024).decode('utf-8') # data는 str type이다
    print("recv: \n", data)
    
#소켓 닫기
client_sock.close()