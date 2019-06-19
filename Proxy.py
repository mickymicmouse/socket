
from socket import *

# 포트넘버와 소켓 작성
tcpSerPort = 8899
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# 서버 소켓을 준비한다.
tcpSerSock.bind(('192.168.2.3', tcpSerPort))
tcpSerSock.listen(5)

while True:
    # 서버준비를 프린트하고, 메세지를 소켓에 저장
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    message = tcpCliSock.recv(4096).decode()

    # 파일 이름을 파싱
    filename = message.split()[1].partition("//")[2].replace('/', '_')
    fileExist = "false"
    try:
        # 파일이 확인 캐시에 존재하면 파일이 존재합니다를 프린트
        f = open(filename, "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('File Exists!')

        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        print('Read from cache')

    # 예외처리
    except IOError:
        print('File Exist: ', fileExist)
        if fileExist == "false":
            #프록시 서버의 소켓을 작성
            print('Creating socket on proxyserver')
            c = socket(AF_INET, SOCK_STREAM)

            hostn = message.split()[1].partition("//")[2].partition("/")[0]
            print('Host Name: ', hostn)
            try:
                # 원격 서버 포트에 연결한다.
                c.connect((hostn, 80))
                print('Socket connected to port 80 of the host')

                c.sendall(message.encode())
                # 메세지를 보내고 버퍼링을 확인한다.
                buff = c.recv(1024)

                tcpCliSock.sendall(buff)
                # 요청파일에 대한 새로운 캐시안에 있는 파일을 만든다.
                # 버퍼의 응답을 클라이언트 소켓으로 보냄.
                # 캐시에 있는 해당파일을 찾는다.
                tmpFile = open("./" + filename, "w")
                tmpFile.writelines(buff.decode().replace('\r\n', '\n'))
                tmpFile.close()

            except:
                print("Illegal request")

        else:
            # 파일에 대한 HTTP응답을 찾을수없을경우
            # 이 내용을 프린트한다
            print('File Not Found...Stupid Andy')
    # 클라이언트와 소켓을 닫는다.
    tcpCliSock.close()
tcpSerSock.close()
