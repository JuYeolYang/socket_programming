import socket
from solve import recevied_data_processing

host = '127.0.0.1'
port = 20000


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((host, port))
server_sock.listen()

client_sock, addr = server_sock.accept()

print("client addr: ", addr)

help = ("==== type ====\n"
        "W: File Write\n"
        "R: File Read and send it\n"
        "C: Circulate\n"
        "N: Sending domain matching ip\n"
        "I: Sending ip matching domain\n"
        "NW: Insert domain, ip into domain_table\n"
        "D: Delete domain address\n"
        "P: show all domain from domain_table\n"
        "\n\n==== input ====\n"
        "COMMAND:Domain or IP(IP or Domain)\n"
        "\n\n==== Example ====\n"
        "W:test.txt(hello) -> Write test.txt hello\n"
        "R:test.txt -> Read test.txt file\n"
        "I:1.1.1.1 -> test1.com\n"
        "N:test2.com -> 2.2.2.2\n"
        "NW:test4.com(4.4.4.4) -> Insert (test4.com, 4.4.4.4) successfully\n"
        "P: -> {'zone': 'test1.com', 'data': '1.1.1.1'} ...\n"
        "D:test3.com -> Delete test3.com successfully\n"
        "C:3+2 -> 5\n"
        "asdf.. -> convert ASCII CODE")

while True:
    
    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
    data = client_sock.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다. 
    if not data:
        break

    decode_data = data.decode('utf-8')
    # 수신받은 문자열을 출력합니다.
    print('Received from', addr, decode_data)
    if decode_data == 'exit':
        break
    
    if decode_data == "--help" or decode_data == "-h":
        send_data = help
    else:
        send_data = recevied_data_processing(decode_data)
    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코) 
    client_sock.sendall(send_data.encode('utf-8'))


# 소켓을 닫습니다.
client_sock.close()
server_sock.close()

