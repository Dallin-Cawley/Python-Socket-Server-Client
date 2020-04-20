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

    # Attempt a Login
    while True:
        if login(client_socket=client_socket):
            while True:
                user_input = raw_input('What would you like to do?\n'
                                       '\t1. Send File\n'
                                       '\t2. New User\n'
                                       '\t3. View Files\n'
                                       '\t4. Quit\n'
                                       'Input: ').lower()

                if user_input == 'quit':
                    body = {
                        'header': 'quit'
                    }

                    client_socket.send(json.dumps(body).encode('UTF-8'))
                    response = json.loads(client_socket.recv(1024).decode('UTF-8'))
                    print(response.get('response'))
                    break

                if user_input == 'send file':
                    file_path = raw_input('What is the file path? ')
                    send_file(client_socket, file_path)

                elif user_input == 'view files':
                    handle_file_view(client_socket=client_socket, requested_directory=os.path.join("C:\\", "Users",
                                                                                                   "lette",
                                                                                                   "PycharmProjects",
                                                                                                   "Python-Socket"
                                                                                                   "-Server-Client",
                                                                                                   "files-received"))
                elif user_input == 'new user':
                    username = raw_input('Username: ')
                    password = raw_input('Password: ')
                    user = raw_input('Name: ')

                    body = {
                        'header': 'new user',
                        'username': username,
                        'password': password,
                        'name': user
                    }

                    client_socket.sendall(json.dumps(body).encode('UTF-8'))

            client_socket.close()
            break
        else:
            print('Username or Password Incorrect\n')


def login(client_socket):
    username = raw_input('Login:\n\tUsername: ')
    password = raw_input('\tPassword: ')

    body = {
        'header': 'login',
        'username': username,
        'password': password
    }

    client_socket.sendall(json.dumps(body).encode('UTF-8'))
    response = json.loads(client_socket.recv(1024).decode('UTF-8'))
    print('Response: ', response.get('response'))
    if response.get('response') == 'true':
        return True
    else:
        return False


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
