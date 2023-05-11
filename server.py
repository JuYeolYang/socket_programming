import pymysql
import socket
from solve import recevied_data_processing

host = '127.0.0.1'
port = 20000
#DB 연결
local_db = pymysql.connect(user = 'root',passwd = 'believeyourself',host = '127.0.0.1',db = 'dns',charset = 'utf8')

db_cursor = local_db.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM domain_table ORDER BY id;"
db_cursor.execute(sql)
result = db_cursor.fetchall()
print(result)
#아직 완성 전

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((host, port))
server_sock.listen()

client_sock, addr = server_sock.accept()

print("client addr: ", addr)

while True:
    
    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
    data = client_sock.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다. 
    if not data:
        break

    decode_data = data.decode('utf-8')
    # 수신받은 문자열을 출력합니다.
    print('Received from', addr, decode_data)
    send_data = recevied_data_processing(decode_data)
    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코) 
    client_sock.sendall(send_data.encode('utf-8'))


# 소켓을 닫습니다.
client_sock.close()
server_sock.close()

