"N:domain.name" <— 형식 지키기
함수 나누기, client 프로그램을 10초 정도 열어두게끔, SQL문 추가

ttl 부분은 db부터 싹다 갈아엎어야해서 마무리 못했습니당..ㅠㅠ 일단 이대로 테스트한 결과입니다

SERVER측

C:\Users\Inconcluso\Desktop\pythonProject9\venv\Scripts\python.exe C:/Users/Inconcluso/Desktop/pythonProject9/main.py
client addr:  ('172.30.1.14', 61047)
Received from ('172.30.1.14', 61047) p
Received from ('172.30.1.14', 61047) N:example.com
Received from ('172.30.1.14', 61047) W:testdata2.com(1.1.1.1)
Received from ('172.30.1.14', 61047) p
Received from ('172.30.1.14', 61047) D:testdata2.com
Received from ('172.30.1.14', 61047) p

Process finished with exit code 0



CLIENT 측

서버에 연결되었습니다.
메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): p
서버 응답: Values in the database:
domain: google.com, ip: 216.58.200.238
domain: facebook.com, ip: 31.13.65.1
domain: testdata.com, ip: 123.45.6.7
domain: example.com, ip: 192.0.2.1

메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): N:example.com
서버 응답: 192.0.2.1
메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): W:testdata2.com(1.1.1.1)
서버 응답: 도메인과 IP 정보가 성공적으로 삽입되었습니다.
메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): p
서버 응답: Values in the database:
domain: google.com, ip: 216.58.200.238
domain: facebook.com, ip: 31.13.65.1
domain: testdata.com, ip: 123.45.6.7
domain: example.com, ip: 192.0.2.1
domain: testdata2.com, ip: 1.1.1.1

메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): D:testdata2.com
서버 응답: 도메인 'testdata2.com'와 해당 IP 주소가 성공적으로 삭제되었습니다.
메시지를 입력하세요 (종료하려면 q 또는 Q를 입력하세요): p
서버 응답: Values in the database:
domain: google.com, ip: 216.58.200.238
domain: facebook.com, ip: 31.13.65.1
domain: testdata.com, ip: 123.45.6.7
domain: example.com, ip: 192.0.2.1

서버를 계속 열어둘 수 없어 이대로 테스트했으며 문제없이 작동했습니다.
