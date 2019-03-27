import socket
import sys
from threading import *
###
# tham số AF_INET cho biết chúng ta sử dụng IP v4, SOCK_TREAM là dùng giao thức TCP.
# Ngoài ra còn một số giá trị khác như AF_INET6 là dùng IP v6, AF_UNIX là chỉ kết nối các ứng dụng trong một máy (không dùng mạng),
# SOCK_DGRAM là dùng giao thức UDP.
###
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define host
host = 'localhost'
 
# define the communication port
port = 8080

# Phương thức bind() chỉ định socket sẽ lắng nghe với địa chỉ IP của máy lấy từ phương thức gethostname() trên cổng 10000.
# Bind the socket to the port
sock.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            sendData = self.sock.recv(1024).decode()
            print('Client sent:', sendData)
            self.sock.send('Oi you sent something to me'.encode())
            if(sendData == "Bye" or sendData == "bye"):
                break

# Phương thức listen() cho python biết socket này là một server,
# tham số của phương thức này là số lượng các kết nối có thể có trong hàng đợi, ít nhất là 0 và cao nhất là do hệ điều hành chỉ định (thường là 5)
# Listen for incoming connections
sock.listen(5)
print("waiting for a connection")
while 1:
    clientsocket, address = sock.accept()
    client(clientsocket, address)
    break
    
sock.close()
# Phương thức accept() sẽ đưa server vào trạng thái chờ đợi 
# cho đến khi có kết nối thì sẽ trả về một tuple gồm có một socket khác dùng để truyền dữ liệu qua lại với client
# và một tuple nữa bao gồm địa chỉ ip và port của ứng dụng client.
# Wait for a connection
# print("waiting for a connection")
# connection, client = sock.accept()
 
# print (client, 'connected')

# Receive the data in small chunks and retransmit it
# Phương thức recv() sẽ đọc các byte dữ liệu có trong socket con,
# tham số 1024 tức là mỗi lần chỉ đọc tối ta 1024 byte dữ liệu
# nên chúng ta đặt trong vòng lặp while để có thể đọc hết những gì client gửi sang
# nếu có dữ liệu gửi sang thì chúng ta gửi trả lời về client thông qua phương thức sendall()
# ở đây chúng ta chỉ đơn giản là gửi lại những gì client đã gửi lên server thôi.
# data = connection.recv(16)
# print ('received ', data)
# if data:
#     connection.sendall(data)
# else:
#     print ('no data from', client)
 
# ngắt kết nối socket nếu không sẽ lãng phí tài nguyên.
# Mặc định thì khi kết thúc một chương trình python thì bộ thu gom rác của python đã tự động ngắt kết nối socket
# nhưng nên tự ngắt thì tốt hơn.
# Close the connection
# connection.close()
