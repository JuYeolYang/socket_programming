import pymysql
import re

class Stack:
    def __init__(self):
        self.top = list()
    def isEmpty(self):
        return len(self.top) == 0
    def size(self):
        return len(self.top)
    def push(self, item):
        self.top.append(item)
    def pop(self):
        if not self.isEmpty():
            return self.top.pop(-1)
        else:
            return None
    def peek(self):
        if not self.isEmpty():
            return self.top[-1]
        
def recevied_data_processing(data:str):
    '''
    ==== type ===="
    W: File Write
    R: File Read and send it
    C: Circulate
    N: Sending domain matching ip
    I: Sending ip matching domain
    NW: Insert domain, ip into domain_table
    D: Delete domain address
    P: show all domain from domain_table
    
    ==== input ===="
    COMMAND:Domain or IP(IP or Domain)
    
    ==== Example ===="
    W:test3.com(3.3.3.3) -> Write domain test3.com
    I:1.1.1.1 -> test1.com
    N:test2.com -> 2.2.2.2
    P: -> {'zone': 'test1.com', 'data': '1.1.1.1'}...
    D:test3.com -> Delete test3.com successfully
    NW:test4.com(4.4.4.4) -> Insert (test4.com, 4.4.4.4) successfully
    C:3+2 -> 5
    '''
    
    command = ('W', 'R', 'C', 'N', 'I', 'NW', 'D', 'P')
    send_data = ""
    if data.find(':') > -1:
        list_data= data.split(':')
        print("list_data: ", list_data)
        #Wrong Command
        if list_data[0].upper() in command[:-1] and list_data[1] == '':
            send_data = "Wrong command. If you need help, Enter -h or --help"
        #file write and read
        elif list_data[0].upper() in command[0:2]:
            #파일 이름
            file_information = list_data[1]
            #file_RW 메소드 반환값
            send_data = file_RW(file_information, list_data[0].upper())
        
        #Circulate
        elif list_data[0].upper() == command[2]:
            send_data = arithmetic_operation(list_data[1])
        
        #Domain, ip
        elif list_data[0].upper() in command[3:]:
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

def file_RW(file_information:str, type:str):
    try:
        send_msg = ""
        #write 인 경우
        if type == 'W':
            #start: 메세지 시작 index, 
            #end: 메세지 끝 index
            start = file_information.find('(')
            end = file_information.find(')')
            #메세지 추출
            msg = file_information[start + 1 : end]
            #파일 이름
            file_name = file_information[:start]
            #print("file_name: ", file_name, ", msg: ", msg)
            try:
                f = open(file_name, 'w') #파일 open
                f.write(msg)
                f.close()
                send_msg = "Message write completed successfully"
                return send_msg
            except:
                send_msg = "File write Error"
                return send_msg
        #read 인 경우
        elif type == 'R':
            try:
                print("file_information: ", file_information)
                f = open(file_information, 'r') #파일 open
                file_data = f.readlines() #파일에 모든 문자열 가지고 오기
                for line in file_data: #각 line 문자열 이어 붙이기
                    send_msg += line
                f.close()
                return send_msg
            except:
                send_msg = "No file: {}".format(file_information)
                return send_msg
                
        else: # 예외처리
            raise Exception("w, r 외의 type이 들어왔습니다.")
    except Exception as e:
        print("Exception: ", e)
        return '0'

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
    db_cursor = local_db.cursor(pymysql.cursors.DictCursor)
    
    #value_type 확인 후 sql문 생성
    #I Command 인 경우
    if value_type == 'I':
        sql = "SELECT * FROM domain_table WHERE data = %s;"
    #N Command 인 경우
    elif value_type == 'N':
        sql = "SELECT * FROM domain_table WHERE zone = %s;"
    #W Command 인 경우
    elif value_type == 'NW':
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
        try:
            db_cursor.execute(sql)
            sql_recive = db_cursor.fetchall()
            
            result_str = ""
            # 값들을 모두 문자열 형태로 변환
            for s in sql_recive: 
                result_str +=  str(s) + '\n'
            return result_str
        except Exception:
            return "error"
        finally:
            db_cursor.close()
            
    elif value_type in ['NW', 'D']: # INSERT, DELETE문 
        try:
            db_cursor.execute(sql, value)
            local_db.commit()
        except pymysql.err.IntegrityError: 
            pass
        finally:
            db_cursor.close()
            
        if value_type == "NW":
            return "Insert " + str(value) + "successfully"
        else:
            return "Delete " + str(value) + "successfully"
    else:
        return "Wrong value type"

#table 생성
def init_table(cursor, db):
    create = "CREATE TABLE IF NOT EXISTS domain_table (id int(11) NOT NULL auto_increment, zone VARCHAR(64) default NULL, data VARCHAR(64) default NULL, PRIMARY KEY(id), KEY(zone), KEY(data), UNIQUE(zone, data));"
    cursor.execute(create)
    
    #test samples
    test_sample = ["INSERT into domain_table (zone, data) VALUES ('test1.com', '1.1.1.1')",
                   "INSERT into domain_table (zone, data) VALUES ('test2.com', '2.2.2.2')"]
    for sql in test_sample:
        try:
            cursor.execute(sql)
        except pymysql.err.IntegrityError as e:
            pass
    db.commit()
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
         
#사칙연산하는 함수            
def arithmetic_operation(expression:str):
    #-, +, *, / , (, )," "이 있으면 그 기준으로 나눈 것을 리스트로 반환
    expression_list = re.split('([-|+|*|/|(|)| ])', expression)
    stack = Stack()
    
    #띄어쓰기 제거
    while True:
        try:
            expression_list.remove(" ")
        except ValueError:
            break
    #공백 제거
    while True:
        try:
            expression_list.remove("")
        except ValueError:
            break
    
    #후기표기법으로 된 리스트값
    postfix_notation = postfix(expression_list)
    
    for item in postfix_notation:
        if item in "-+*/":
            op2 = stack.pop()
            op1 = stack.pop()
            #연산자가 연속으로 들어간 경우
            if op1 is None or op2 is None:
                return "입력한 식이 잘못되었습니다(op1 or op2 is None)"
            if item == '-':
                op = float(op1) - float(op2)
                stack.push(op)
            elif item == '+':
                op = float(op1) + float(op2)
                stack.push(op)
            elif item == '*':
                op = float(op1) * float(op2)
                stack.push(op)
            else: #0으로 나눈 경우
                if float(op2) == 0:
                    return "0으로 나누었습니다. 오류 발생"
                op = float(op1) / float(op2)
                stack.push(op)
        else:
            stack.push(item)
    result = stack.pop()
    
    if not stack.isEmpty(): # 연산자 없이 숫자를 입력한 경우
        return "입력한 식이 잘못 입력되었습니다(Stack is not Empty)"
    else:
        return str(result)

#후기표기법으로 바꿔주는 함수
def postfix(queue:list):
    #연산 우선순위
    op = {'-': 1, '+': 1, '*': 2, '/':2, '(': 0, ')': 0}
    stack = Stack()
    result = list()
    
    for item in queue:
        if item in '(':
            stack.push('(')
        elif item in ')':
            while not stack.isEmpty():
                pop_item = stack.pop()
                if pop_item in '(':
                    break
                else:
                    result.append(pop_item)
        elif item in "-+*/":
            while not stack.isEmpty():
                stack_top_item = stack.peek()
                if op[item] <= op[stack_top_item]:
                    result.append(stack_top_item)
                    stack.pop()
                else:
                    break
            stack.push(item)
        else:
            result.append(item)
        
    while not stack.isEmpty():
        item = stack.pop()
        result.append(item)
    
    return result