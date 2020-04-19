import os
import socket
from pip._vendor.distlib.compat import raw_input
import json


def main():
    # Create a socket
    client_socket = socket.socket()

    # Connect to remote host
    client_socket.connect((socket.gethostname(), 8001))
    print(client_socket.recv(1024).decode('UTF-8'), '\n')

    # Send some information to the host.
    user_input = raw_input('What would you like to do?\n'
                           '\t1. Send File\n'
                           '\t2. Send Message\n'
                           '\t3. Quit\n'
                           '\t4. View Files\n'
                           'Input: ').lower()

    while True:

        if user_input == 'quit':
            body = {
                'header': 'quit'
            }

            client_socket.send(json.dumps(body).encode('UTF-8'))
            print(client_socket.recv(1024).decode('UTF-8'))
            break

        if user_input == 'send file':
            file_path = raw_input('What is the file path? ')
            send_file(client_socket, file_path)

        elif user_input == 'send message':
            user_input = raw_input('What is the Message? ')

            body = {
                'header': 'message',
                'message': user_input
            }

            client_socket.send(json.dumps(body).encode('UTF-8'))
            message = ''
            while message != 'end':
                message = client_socket.recv(1024).decode('UTF-8')
                print(message)

        elif user_input == 'view files':
            handle_file_view(client_socket=client_socket, requested_directory=os.path.join("C:\\", "Users", "lette",
                                                                                           "PycharmProjects",
                                                                                           "Python-Socket-Server-Client",
                                                                                           "files-received"))

        user_input = raw_input('\nWhat would you like to do?\n\t1. Send File\n\t2. Send Message\n\t3. Quit\nInput: ')

    client_socket.close()


def send_file(client_socket, file_name):
    try:
        file_path = os.path.abspath(file_name)
        file_size = os.path.getsize(file_path)
        body = {
            'header': 'file',
            'file_type': os.path.splitext(file_path)[1],
            'file_name': os.path.basename(file_path),
            'file_size': file_size,
            'directory': 'files-received'
        }

        file = open(file_path, 'rb')

        file_bytes = file.read(file_size)
        file.close()

        client_socket.sendall(json.dumps(body).encode('UTF-8'))
        client_socket.sendall(file_bytes)

        print(client_socket.recv(1024).decode('UTF-8'))
    except FileNotFoundError:
        print('File not found. Try again.')
        pass


def handle_file_view(client_socket, requested_directory):
    body = {
        'header': 'ls',
        'current_directory': requested_directory
    }

    client_socket.sendall(json.dumps(body).encode('UTF-8'))
    current_directory_list = client_socket.recv(1024).decode('UTF-8')
    print(current_directory_list)


if __name__ == '__main__':
    main()
