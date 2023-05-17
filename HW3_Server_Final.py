import socket
import pymysql
import threading

# MySQL 연결 설정
db = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="DNS"
)

# DNS 테이블 생성
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS DNS (domain VARCHAR(255), ip VARCHAR(255))")

# 서버 설정
HOST = '0.0.0.0'
PORT = 8000

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('DNS 서버가 시작되었습니다.')

def handle_client(client_socket):
    while True:
        # 클라이언트 요청 수신
        request = client_socket.recv(1024).decode()

        # 요청 처리
        if request.startswith('INSERT'):
            # INSERT 요청 처리
            _, domain, ip = request.split()
            sql = f"INSERT INTO DNS (domain, ip) VALUES (%s, %s)"
            values = (domain, ip)
            cursor.execute(sql, values)
            db.commit()
            response = 'DNS 데이터가 추가되었습니다.'
        elif request.startswith('UPDATE'):
            # UPDATE 요청 처리
            _, domain, ip = request.split()
            sql = f"UPDATE DNS SET ip = %s WHERE domain = %s"
            values = (ip, domain)
            cursor.execute(sql, values)
            db.commit()
            if cursor.rowcount > 0:
                response = 'DNS 데이터가 수정되었습니다.'
            else:
                response = '해당 도메인이 존재하지 않습니다.'
        elif request.startswith('DELETE'):
            # DELETE 요청 처리
            _, domain = request.split()
            sql = "DELETE FROM DNS WHERE domain = %s"
            values = (domain,)
            cursor.execute(sql, values)
            db.commit()
            if cursor.rowcount > 0:
                response = 'DNS 데이터가 삭제되었습니다.'
            else:
                response = '해당 도메인이 존재하지 않습니다.'
        elif request.startswith('QUERY'):
            # QUERY 요청 처리
            _, domain = request.split()
            sql = "SELECT ip FROM DNS WHERE domain = %s"
            values = (domain,)
            cursor.execute(sql, values)
            result = cursor.fetchone()
            if result is not None:
                response = f'{domain}의 IP 주소: {result[0]}'
            else:
                response = '해당 도메인이 존재하지 않습니다.'
        elif request == 'SEARCH ALL':
            # SEARCH ALL 요청 처리
            sql = "SELECT domain, ip FROM DNS"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) > 0:
                response = 'DNS 데이터 검색 결과:\n'
                for row in results:
                    response += f'{row[0]}: {row[1]}\n'
            else:
                response = 'DNS 데이터가 존재하지 않습니다.'
        else:
            response = '잘못된 요청입니다.'

        # 클라이언트에 응답 전송
        client_socket.sendall(response.encode())

        # 클라이언트와의 연결 종료
        if request == 'DISCONNECT':
            break

    client_socket.close()

while True:
    # 클라이언트로부터 연결 요청 대기
    client_socket, addr = server_socket.accept()
    print('클라이언트가 연결되었습니다:', addr)

    # 클라이언트 요청을 처리하는 스레드 생성
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

