import pymysql

def received_data_processing(data: str):
    # 지원하는 명령어
    command = ('N', 'I', 'W', 'P', 'D')  # Add 'D' command
    send_data = ""

    if data[0].upper() == 'P':
        send_data = convert_domain_ip("P", 'P')
    elif data.find(':') > -1:
        list_data = data.split(':')
        if list_data[0].upper() in command:
            value_type = list_data[0].upper()
            value = list_data[1]
            send_data = convert_domain_ip(value, value_type)
        else:
            send_data = list_data[0] + " command is not supported."
    return send_data

def convert_domain_ip(value: str, value_type: str):
    local_db = pymysql.connect(user='root',
                               passwd='1234',
                               host='localhost',
                               database='dns',
                               charset='utf8')
    db_cursor = local_db.cursor()

    if value_type.upper() == 'I':
        # value는 IP 주소이며, 해당 IP 주소에 대응하는 도메인을 찾아 반환합니다.
        query = "SELECT domain FROM DNS WHERE ip = %s"
        db_cursor.execute(query, (value,))
        result = db_cursor.fetchone()
        if result:
            return result[0]  # 첫 번째 결과 반환
        else:
            return "해당 IP 주소에 대응하는 도메인이 없습니다."
    elif value_type.upper() == 'N':
        # value는 도메인 이름이며, 해당 도메인에 대응하는 IP 주소를 찾아 반환합니다.
        query = "SELECT ip FROM DNS WHERE domain = %s"
        db_cursor.execute(query, (value,))
        result = db_cursor.fetchone()
        if result:
            return result[0]  # 첫 번째 결과 반환
        else:
            return "해당 도메인에 대응하는 IP 주소가 없습니다."
    elif value_type.upper() == 'W':
        # value는 "도메인(IP)" 형식으로 주어지며, 해당 정보를 MySQL의 DNS 테이블에 삽입합니다.
        domain, ip = value.split('(')[0], value.split('(')[1].rstrip(')')
        query = "INSERT INTO DNS (domain, ip) VALUES (%s, %s)"
        db_cursor.execute(query, (domain, ip))
        local_db.commit()
        return "도메인과 IP 정보가 성공적으로 삽입되었습니다."
    elif value_type.upper() == 'P':
        # DNS 테이블에 존재하는 모든 도메인과 IP 주소를 반환합니다.
        query = "SELECT domain, ip FROM DNS"
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        values_str = "Values in the database:\n"
        for row in results:
            values_str += f"domain: {row[0]}, ip: {row[1]}\n"
        if results:
            return values_str
        else:
            return "DNS 테이블에 등록된 도메인과 IP 주소가 없습니다."
    elif value_type.upper() == 'D':
        # value는 도메인 이름이며, 해당 도메인과 해당 IP 주소를 DNS 테이블에서 삭제합니다.
        query = "DELETE FROM DNS WHERE domain = %s"
        db_cursor.execute(query, (value,))
        local_db.commit()
        return f"도메인 '{value}'와 해당 IP 주소가 성공적으로 삭제되었습니다."
    else:
        return "유효하지 않은 값 유형입니다."
