import socket
import log
import _thread

class Proxy:
    '''
    Nhận requests từ web browser
    Kiểm tra tính hợp lệ
    Gửi requests đi cho web server
    Khi có được dữ liệu từ web server thì gửi lại cho trình duyệt
    '''
    MAX_DATA = 4096
    host = ""
    port = 0
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @staticmethod
    def __communicate(self, host, conn, requests):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 80))
            s.send(requests)

            while True:
                data = s.recv(self.MAX_DATA)
                #print(data)
                if (len(data) > 0):
                    conn.sendall(data)
                else:
                    break

            s.close()
        except TimeoutError:
            s.close()
        

    @staticmethod
    def __client_thread(self, conn, addr):
        requests = conn.recv(self.MAX_DATA)
        url = self.parse_url(requests.decode('ASCII'))
        # LOG to file to see what happened
        print('URL: ', url)
        #print(requests)
        # Get server ip
        webserver = socket.gethostbyname(url)
        self.__communicate(self, webserver, conn, requests)
        conn.close()


    def parse_url(self, requests):
        first_line = requests.split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos + 3):]
        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if (webserver_pos == -1):
            webserver_pos = len(temp)
        webserver = ""
        if (port_pos == -1 or webserver_pos < port_pos):
            webserver = temp[:webserver_pos]
        else:
            webserver = temp[:port_pos]

        return webserver

        # attrs = first_line.split(' ')
        # print(len(attrs))
        # if (len(attrs) >= 1):
        #     url = attrs[1]
        #     return attrs[1].split('/')[2]

        # return attrs[0]#.split('/')[2]

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(False)

        while True:
            conn, addr = self.server.accept()
            _thread.start_new_thread(self.__client_thread, (self, conn, addr))

    def close(self):
        self.server.close()

    

