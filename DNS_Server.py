import socket
import pymysql
import time
import threading

# Set socket
HOST = 'localhost'
PORT = 50000     

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, addr = server_socket.accept()

print('Connected by', addr)


# Connect DB
conn = pymysql.connect (host='localhost', port=3307, user='root', password='0000', db='PJ_DNS')
cursor = conn.cursor()

# Authoritative DNS
create1_sql = "CREATE TABLE Authoritative_DNS_ROOT(ip varchar(255) NOT NULL, domain_name varchar(255));"
create2_sql = "CREATE TABLE Authoritative_DNS_SUB(root_domain varchar(255) NOT NULL, ip varchar(255) NOT NULL, domain_name varchar(255));"
# Cache DNS
create3_sql = "CREATE TABLE Cache_DNS(ip varchar(255), domain_name varchar(255));"
# Execute query
cursor.execute(create1_sql)
cursor.execute(create2_sql)
cursor.execute(create3_sql)

# input info
"""
input form: Command1/Command2/TTL/Domain name/IPV4/Ref
input Write-Root ex: W/Root/0/dankook.ac.kr/220.69.176.17
input Write-Sub ex: W/Sub/0/lib.dankook.ac.kr/220.149.241.5/dankook.ac.kr (*Ref = root domain name)
input Type ex: T/A/10/dankook.ac.kr//, T/CNAME/10/dankook.ac.kr//
"""

# 입력값 나눠서 레코드 타입별 명령 수행
def findCommand(input: str):
    inputs = input.split("/")
    command1 = inputs[0]
    command2 = inputs[1]
    ttl = int(inputs[2])
    domain_name = inputs[3]
    ip = inputs[4]

    if(command1 == "W"):
        if(command2 == "Root"):
            return writeRoot(ip, domain_name)
        else:
            return writeSub(ip, domain_name, inputs[5])
    elif(inputs[0] == "T"):
        if(command2 == "A"):
            return type_A(ttl, domain_name)
        else:
            return type_CNAME(ttl, domain_name)
    else:
        print("Command1 does not exist")


# Write Root domain
def writeRoot(ip: str, domain: str):
    print(ip)
    print(domain)
    cursor.execute("INSERT INTO Authoritative_DNS_ROOT (ip, domain_name) VALUES (%s, %s)", (ip, domain))
    conn.commit()
    return "Query executed-Root written"

# Write Subdomain
def writeSub(ip: str, domain: str, root_domain: str):
    cursor.execute("INSERT INTO Authoritative_DNS_SUB (root_domain, ip, domain_name) VALUES (%s, %s, %s)", (root_domain, ip, domain))
    conn.commit()
    return "Query executed-Sub written"

data = ""
# Record type A, returns IPV4
def type_A(ttl: int, domain: str):
    cursor.execute("SELECT * FROM Authoritative_DNS_ROOT WHERE domain_name = %s", domain)
    rows = cursor.fetchone()
    if(rows == None):
        cursor.execute("SELECT * FROM Authoritative_DNS_SUB WHERE domain_name = %s", domain)
        rows = cursor.fetchone()
    cursor.execute("INSERT INTO Cache_DNS VALUES (%s, %s)",(rows[0], domain))
    conn.commit()
    
    t = threading.Thread(target=timer(ttl))
    t.start()

    return rows[0]
  

# Record type CNAME, returns subdomain
def type_CNAME(ttl: int, root_domain: str):
    cursor.execute("SELECT domain_name FROM Authoritative_DNS_SUB WHERE root_domain = %s", root_domain)
    rows = cursor.fetchone()
    cursor.execute('INSERT INTO Cache_DNS VALUES ("Empty", %s)', rows[0])
    conn.commit()
    
    t = threading.Thread(target=timer(ttl))
    t.start()

    return rows[0]

# Timer Thread
def timer(sec: int):
    while (sec != 0):
        sec -= 1
        time.sleep(1)
        print(sec)
    # Implement TTL
    cursor.execute("TRUNCATE table Cache_DNS;")
    conn.commit()
    print("Query executed-Cache deleted")


# Receive & Send data
while True: 
    data = client_socket.recv(1024) 
    if not data:
        break
    print('Received from', addr, data.decode())
    output = findCommand(data.decode('utf-8'))
    client_socket.sendall(output.encode())

conn.close()
client_socket.close()
server_socket.close()


