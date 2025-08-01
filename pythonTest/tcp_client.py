import socket
import time
# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버의 호스트와 포트 설정
host = '192.168.131.201'
port = 9009

# 서버에 연결
client_socket.connect((host, port))
print("서버에 연결되었습니다.")

# def check_connection(host, port, timeout=1):
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(timeout)
#         result = sock.connect_ex((host, port))
#         sock.close()
#         return result == 0  # 0이면 연결 성공
#     except Exception as e:
#         print(f"Error: {e}")
#         return False

# if check_connection(host, port):
#     print("연결 성공")
# else:
#     print("연결 실패")

# 데이터 전송
# while True:
#     command = "CLS:SetVolt"
#     voltage = 1.23
#     message = f"{command} {voltage}\r\n"
#     client_socket.send(message.encode())

    # 데이터 수신
    # data = client_socket.recv(1024).decode()
    # print(f"받은 데이터: {data}")
    # time.sleep(0.01)

command = "CLS:GetCount"
count = client_socket.send(command.encode())
print(count)
# 소켓 종료
client_socket.close()
