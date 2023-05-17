import pymysql
def recevied_data_processing(data:str):
    command = ('N', 'I', 'W')
    send_data = ""
    if data.find(':') > -1:
        list_data= data.split(':')
        #Domain, ip
        if list_data[0].upper() in command:
            value_type = list_data[0].upper()
            value = list_data[1]
            send_data = convert_domain_ip(value, value_type)
        #command가 잘못 입력된 경우
        else:
            send_data = list_data[0] + " command is unable."
    else:
        #메세지를 ASCII코드로 변환한 값을 문자열로 전송
        for alphbet in data:
            send_data += str(ord(alphbet)) + " "
        
        print("send_data: ",send_data)
    
    return send_data

def convert_domain_ip(value: str, value_type:str):
    #value_type와 mysql의 colunm value랑 매핑
    value_dict = {'I': 'data', 'D': 'zone'}
    #DB 연결
    local_db = pymysql.connect(user = 'socket',
                               passwd = 'Sprogramming212@!@',
                               host = '127.0.0.1',
                               db = 'dns',
                               charset = 'utf8')
    #table 생성 후 cursor 받기
    db_cursor = init_table(local_db)
    
    '''
    result type
        -1: Error
         0: value_type = W
      None: value_type = I, D
    '''
    result = None
    #value_type 확인 후 sql문 생성
    #I Command 인 경우
    if value_type == 'I':
        sql = "SELECT * FROM domain_table WHERE data = %s;"
    #D Command 인 경우
    elif value_type == 'N':
        sql = "SELECT * FROM domain_table WHERE zone = %s;"
    #W Command 인 경우
    elif value_type == 'W':
        start = value.find("(")
        end = value.find(")")
        ip = value[start + 1:end]
        domain = value[:start]
        value = (domain, ip)
        sql = "INSERT into domain_table (zone, data) VALUES (%s, %s)"
        print(sql, "\n", value)
        result = 0
    #Error 처리
    else:
        result = -1
        return "Wrong value type"
    
    try:
        db_cursor.execute(sql, value)
        db_cursor.close()
    #이미 테이블에 값이 들어가있는 경우
    except pymysql.err.IntegrityError as e:
        pass
    
    #error 처리
    if result == -1:
        return "There is no {} in DNS".format(value)
    #INSERT 처리
    elif result == 0:
        local_db.commit()
        return "finish"
    #SELECT 처리
    else:
        result = db_cursor.fetchall()
        result_dict = result[0]
        print(result, result_dict)
        return result_dict[value_dict[value_type]]

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