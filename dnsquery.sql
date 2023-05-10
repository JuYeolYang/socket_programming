-- DB생성
 CREATE database DNS;
 USE DNS;
 -- 테이블 생성
CREATE TABLE domains (
  id INT NOT NULL AUTO_INCREMENT,
  domain VARCHAR(255) NOT NULL,
  ip VARCHAR(255) NOT NULL,
  ttl INT NOT NULL,
  PRIMARY KEY (id)
);

 -- 테스트할 데이터 삽입
INSERT INTO domains (domain, ip, ttl) VALUES
	('example.com', '192.0.2.1', 3600),
    ('google.com', '216.58.200.238', 300),
    ('facebook.com', '31.13.65.1', 7200);
    
    
    
--mysql을 사용하여 미리 데이터베이스와 테이블을 만들어두지 않는다면? 지금의 오류 발생하지 않을 가능성O
