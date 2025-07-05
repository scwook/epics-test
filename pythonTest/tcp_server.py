import socket

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 호스트와 포트 설정
host = 'localhost'
port = 12345

# 소켓 바인딩
server_socket.bind((host, port))

# 연결 수신 대기
server_socket.listen(5)
print("서버가 시작되었습니다. 연결을 기다리는 중...")

# 클라이언트 연결 수락
client_socket, addr = server_socket.accept()
print(f"연결됨: {addr}")

# 데이터 수신
data = client_socket.recv(1024).decode()
print(f"받은 데이터: {data}")

# 데이터 전송
message = "데이터를 받았습니다."
client_socket.send(message.encode())

# 소켓 종료
client_socket.close()
server_socket.close()
