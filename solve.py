import pymysql
def recevied_data_processing(data:str):
    command = ('D', 'I')
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
    local_db = pymysql.connect(user = 'root',passwd = 'believeyourself',host = '127.0.0.1',db = 'dns',charset = 'utf8')
    db_cursor = local_db.cursor(pymysql.cursors.DictCursor)
    
    #value_type 확인 후 sql문 생성
    if value_type == 'I':
        sql = "SELECT * FROM domain_table WHERE data = %s;"
    elif value_type == 'D':
        sql = "SELECT * FROM domain_table WHERE zone = %s;"
    else:
        return "Wrong value type"
    
    db_cursor.execute(sql, value)
    result = db_cursor.fetchall()
    result_dict = result[0]
    print(result, result_dict)
    db_cursor.close()
    
    if result is None:
        return "There is no {} in DNS".format(value)
    else:
        return result_dict[value_dict[value_type]]
