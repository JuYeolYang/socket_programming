import pymysql
conn = pymysql.connect (host='localhost', port=3307, user='root', password='0000', db='teampj_db')

cursor = conn.cursor()

create_sql = "CREATE TABLE basic(ip varchar(255) PRIMARY KEY NOT NULL, domain_name varchar(255));"
insert_sql = "INSERT INTO basic VALUES ('172.217.25.174', 'google.com'), ('142.250.206.238', 'youtube.com'), ('205.251.242.103', 'amazon.com');"

cursor.execute(create_sql)
cursor.execute(insert_sql)
conn.commit()

conn.close()