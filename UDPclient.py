from socket import *
import time

serverName = '192.168.xxx.xxx' # 서버 주소
serverPort = 12000 # 서버에 지정된 서버 포트
clientSocket = socket(AF_INET, SOCK_DGRAM) # IPv4를 사용하여 udp소켓을 지정함
clientSocket.settimeout(1) # 소켓의 제한시간을 설정

for i in range(0, 10):
	sendTime = time.time()
	message = ('Ping %d %s' % (i+1, sendTime)).encode() # 메세지를 전달하는 데이터 패킷을 생성
	try:
		clientSocket.sendto(message, (serverName, serverPort)) # 서버에 송신
		modifiedMessage, serverAddress = clientSocket.recvfrom(1024) # 서버로 부터 정보와 주소를 수신한다.
		rtt = time.time() - sendTime # 왕복시간을 산출한다.
		print('Sequence %d: Reply from %s    RTT = %.3fs' % (i+1, serverName, rtt))#순서와 서버주소와 왕복시간을 프린트한다.
	except Exception as e: #예외 값을 지정
		print('Sequence %d: Request timed out' % (i+1))#왕복시간이 1초이상이된다면 타임아웃을 프린트
		
clientSocket.close() #소켓을 닫는다.
