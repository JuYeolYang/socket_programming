import pymysql
def recevied_data_processing(data:str):
    '''
    ==== type ===="
    N: Sending domain matching ip
    I: Sending ip matching domain
    NW: Insert domain, ip into domain_table
    D: Delete domain address
    P: show all domain from domain_table
    
    ==== input ===="
    COMMAND:Domain or IP(IP or Domain)
    
    ==== Example ===="
    I:1.1.1.1 -> test1.com
    N:test2.com -> 2.2.2.2
    P: -> {'zone': 'test1.com', 'data': '1.1.1.1'}...
    D:test3.com -> Delete test3.com successfully
    W:test4.com(4.4.4.4) -> Insert (test4.com, 4.4.4.4) successfully
    '''
    command = ('N', 'I', 'W', 'D', 'P')
    send_data = ""
    if data.find(':') > -1:
        list_data= data.split(':')
        print("list_data: ", list_data)
        #Wrong Command
        if list_data[0].upper() in command[:-1] and list_data[1] == '':
            send_data = "Wrong command. If you need help, Enter -h or --help"
        
        #Domain, ip
        elif list_data[0].upper() in command:
            value_type = list_data[0].upper()
            value = None
            if value_type == 'P':
                value = None
            else:
                value = list_data[1]
            send_data = convert_domain_ip(value, value_type)
        #command가 잘못 입력된 경우
        else:
            send_data = list_data[0] + " command is unable."
    else:
        send_data = "ASCII CODE: "
        #메세지를 ASCII코드로 변환한 값을 문자열로 전송
        for alphbet in data:
            send_data += str(ord(alphbet)) + " "
        
    print("send_data: ",send_data)
    return send_data

def convert_domain_ip(value: str, value_type:str):
    #value_type와 mysql의 colunm value랑 매핑
    value_dict = {'I': 'zone', 'N': 'data'}
    #DB 연결
    local_db = pymysql.connect(user = 'socket',
                               passwd = 'Sprogramming212@!@',
                               host = '127.0.0.1',
                               db = 'dns',
                               charset = 'utf8')
    #table 생성 후 cursor 받기
    db_cursor = init_table(local_db)

    #value_type 확인 후 sql문 생성
    #I Command 인 경우
    if value_type == 'I':
        sql = "SELECT * FROM domain_table WHERE data = %s;"
    #N Command 인 경우
    elif value_type == 'N':
        sql = "SELECT * FROM domain_table WHERE zone = %s;"
    #W Command 인 경우
    elif value_type == 'W':
        #ip 시작주소와 마지막 주소 찾기
        start = value.find("(")
        end = value.find(")")
        
        if start < 0 or end < 0:
            return "NW command argument is not match. please keep the format.\nex)NW:Domain(Ip)"
        
        ip = value[start + 1:end]
        if not check_ip(ip): #ip 형식 검사
            return "Ip format Error: format is incorrect. IP range is 0.0.0.0 ~ 255.255.255.255"
        domain = value[:start]
        value = (domain, ip)
        
        sql = "INSERT into domain_table (zone, data) VALUES (%s, %s)"
    #P Command 인 경우
    elif value_type == 'P':
        sql = "SELECT zone, data FROM domain_table;"
    #D Command 인 경우
    elif value_type == 'D':
        sql = "DELETE FROM domain_table WHERE zone = %s"
    #Error 처리
    else:
        return "Wrong value type"
    
    # execute sql
    # 동일한 동작을 하는 명령어끼리 묶음
    if value_type in ['I', 'N']: #SELECT문
        
        if value_type == 'I' and not check_ip(str(value)): #ip 형식 검사
            return "Ip is not Error: format is incorrect"
        
        db_cursor.execute(sql, value) # sql문 전송
        sql_recive = db_cursor.fetchall() # 받아온 데이터
        db_cursor.close()
        
        if sql_recive == ():
            return str(value) + " 값은 찾을 수 없습니다"
        else:
            result_dict = sql_recive[0] # 원하는 데이터는 0번째에 있다
            print("result_dict: ", result_dict)
            return result_dict[value_dict[value_type]]
    elif value_type == 'P': # domain_table에 있는 엔티티 출력
        db_cursor.execute(sql)
        sql_recive = db_cursor.fetchall()
        db_cursor.close()
        
        result_str = ""
        # 값들을 모두 문자열 형태로 변환
        for s in sql_recive: 
            result_str +=  str(s) + '\n'
        return result_str
    elif value_type in ['W', 'D']: # INSERT, DELETE문 
        try:
            db_cursor.execute(sql, value)
            local_db.commit()
            db_cursor.close()
        except pymysql.err.IntegrityError: 
            pass
        if value_type == "W":
            return "Insert " + str(value) + "successfully"
        else:
            return "Delete " + str(value) + "successfully"
    else:
        return "Wrong value type"
    
#table 생성
def init_table(db: pymysql.connect):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    create = "CREATE TABLE IF NOT EXISTS domain_table (id int(11) NOT NULL auto_increment, zone VARCHAR(64) default NULL, data VARCHAR(64) default NULL, PRIMARY KEY(id), KEY(zone), KEY(data), UNIQUE(zone, data));"
    cursor.execute(create)
    
    #test samples
    test_sample = ["INSERT into domain_table (zone, data) VALUES ('test1.com', '1.1.1.1')",
                   "INSERT into domain_table (zone, data) VALUES ('test2.com', '2.2.2.2')"]
    for sql in test_sample:
        try:
            cursor.execute(sql)
            db.commit()
        except pymysql.err.IntegrityError as e:
            pass
    return cursor

# ip형식을 지켰는지 검사하는 함수
def check_ip(ip:str):
    ip_list = ip.split(".")
    print(ip_list)
    # ip는 0.0.0.0 ~ 255.255.255.255사이의 값을 가진다
    # 만약 256.0.0.1이나 -1.-1.0.0 같은 ip값은 가질 수 없기 때문에 이 부분은 확인해 주어야한다
    # 입력된 ip 범위가 넘어갔는지 확인
    
    if len(ip_list) != 4:
        return False
    for number in ip_list:
        try:
            if int(number) in range(0, 256):
                pass
            else:
                return False
        except ValueError:
            return False
    return True
         