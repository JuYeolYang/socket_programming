def recevied_data_processing(data:str):
    command = ('W', 'R', 'C', 'D', 'I')
    send_data = ""
    if data.find(':'):
        list_data= data.split(':')
        #file write
        if list_data[0].upper() == command[0]:
            #start: 메세지 시작 index, 
            #end: 메세지 끝 index
            start = list_data[1].find('(')
            end = list_data[1].find(')')
            #메세지 추출
            msg = list_data[1][start + 1 : end]
            #파일 이름
            file_name = list_data[1][:start]
            #file_RW 메소드 반환값
            send_data = file_RW(file_name, 'w', msg)
        
        #file read
        elif list_data[0].upper() == command[1]:
            #파일 이름
            file_name = list_data[1]
            #file_RW 메소드 반환값
            send_data = file_RW(file_name, 'r')
        
        #Circulate
        elif list_data[0].upper() == command[2]:
            send_data = arithmetic_operation(list_data[1])
        
        #Domain
        elif list_data[0].upper() == command[3]:
            return 0
        #ip
        elif list_data[0].upper() == command[4]:
            return 0
        #command가 잘못 입력된 경우
        else:
            send_data = list_data[0] + " command is unable."
    else:
        #메세지를 ASCII코드로 변환한 값을 문자열로 전송
        for alphbet in data:
            send_data += str(ord(alphbet)) + " "
        
        print("send_data: ",send_data)
    
    return send_data

def file_RW(file_name:str, type:str, msg = None):
    try:
        #write 인 경우
        if type == 'w':
            f = open(file_name, 'w') #파일 open
            f.write(msg)
            f.close()
            return "Message write completed successfully"
        #read 인 경우
        elif type == 'r':
            send_msg = ""
            f = open(file_name, 'r') #파일 open
            file_data = f.readlines() #파일에 모든 문자열 가지고 오기
            for line in file_data: #각 line 문자열 이어 붙이기
                send_msg += line
            f.close()
            return send_msg
        
        else: # 예외처리
            raise Exception("w, r 외의 type이 들어왔습니다.")
    except Exception as e:
        print("Exception: ", e)

def arithmetic_operation(expression:str):
    
    postfix_notation = postfix()
    return 0
def postfix(queue:list):
    return 0