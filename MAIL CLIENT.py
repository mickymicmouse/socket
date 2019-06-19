from socket import *

# 메일 내용 작성
subject = "difficult!"
contenttype = "text/plain"
msg = "difficult!"
endmsg = "\r\n.\r\n"

# 메일서버를 선택하고 smtp사용 
mailserver = "smtp.gmail.com"

# 보내는사람과 받는사람을 설정
fromaddress = ""
toaddress = ""

# 아이디와 패스워드 입력(인증정보)
username = ""
password = ""

# 클라이언트 소켓을 만들고 메일서버와 tcp연결을 한다.
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((mailserver, 25))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# helo명령을 보내고 서버응답을 출력한다.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# 로그인 정보를 보낸다.
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')
#유저 아이디를 보낸다
clientSocket.sendall((username + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')
#패스워드를 보낸다
clientSocket.sendall((password + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '235'):
	print('235 reply not received from server')

# 보내는사람의 주소와 서버응답을 보낸다.
clientSocket.sendall(('MAIL FROM: <' + fromaddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

# 받는사람의 주소와 서버응답을 보낸다.
clientSocket.sendall(('RCPT TO: <' + toaddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

# Send DATA command and print server response.
clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '354'):
	print('354 reply not received from server')

# 메세지를 보낸다.
message = 'from:' + fromaddress + '\r\n'
message += 'to:' + toaddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contenttype + '\t\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

# 마침표 메세지를 보낸다.
clientSocket.sendall(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

# 나가는 명령을 내리고 서버의 반응을 받는다.
clientSocket.sendall('QUIT\r\n'.encode())

# 연결을 끊는다
clientSocket.close()
