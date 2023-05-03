from socket import *

s = socket()
address = ('localhost', 9999)
s.bind(address)
s.listen()
print('Waiting for clients...')
conn, address = s.accept()
print("connected by", address)

while True:
    try:
        data = conn.recv(1024)  #수신할 때 예외

    except Exception as e:
        print("Exeption Break")
        conn.close()
        break
    else:
        text = data.decode()
        ascii_values = ""
        for i in text:
            ascii_values=ascii_values+" "+str(ord(i))
        print(ascii_values)
    try:
        conn.send(ascii_values.encode('utf-8'))
    except:
        conn.close()
        break