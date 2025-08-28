import socket
import time

SERVER_IP = "192.168.131.219"
SERVER_PORT = 9000
MESSAGE_SIZE = 24

def pad_message(msg):
    data = msg.encode()
    if len(data) < MESSAGE_SIZE:
        data += b' ' * (MESSAGE_SIZE - len(data))
    return data[:MESSAGE_SIZE]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.connect((SERVER_IP, SERVER_PORT))

while True:
     command = "CLS:SetVolt"
     voltage = 1.23
     message = f"{command} {voltage}"
     data = pad_message(message)
     s.sendall(data)

     command = "CLS:SetClrCount"
     data = pad_message(command)
#     s.sendall(data)

     command = "CLS:GetCount"
     message = f"{command}"
     data = pad_message(message)
     s.sendall(data)
     
     recv_data = s.recv(MESSAGE_SIZE)
     print(f"Receive: {recv_data}")

     time.sleep(1)

#for m in messages:
#    data = pad_message(m)
#    s.sendall(data)  # 연속 전송
#    print(f"Sent: {data}")

# 서버 echo 수신
#for _ in messages:
#    recv_data = s.recv(MESSAGE_SIZE)
#    print(f"Received: {recv_data}")

s.close()

