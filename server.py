import socket
from _thread import *
from pip._vendor.distlib.compat import raw_input
import json
import os
from security import security


def main():
    # Create a socket
    server_socket = socket.socket()

    # Bind the socket to a port for use
    server_socket.bind((socket.gethostname(), 8001))

    # Listen for a connection
    server_socket.listen()

    # Begin servicing client's
    start_new_thread(handle_connections, (server_socket,))

    while True:
        user_input = raw_input("Shut down: ")

        if user_input == 'yes':
            server_socket.close()
            break


def handle_connections(server_socket):
    # Accept an incoming connection
    while True:
        connection, con_address = server_socket.accept()
        start_new_thread(handle_client_connection, (connection,))


def handle_client_connection(client_connection):
    # Handle the connection
    data = 'Connection Accepted'.encode('UTF-8')
    client_connection.send(data)

    while True:
        data = client_connection.recv(1024)
        request_body = json.loads(data)
        header = request_body.get('header')

        # When the Client wishes to disconnect
        if header == 'quit':
            response_data = 'Connection Terminating'
            client_connection.send(response_data.encode('UTF8'))
            break

        # If the client wishes to manipulate files
        if header == 'file':
            handle_file(request_body=request_body, client_connection=client_connection)
            client_connection.send('File saved'.encode('UTF-8'))

        # If the client wishes to just send a message
        elif header == 'message':
            client_connection.send(('You sent: ' + request_body.get('message')).encode('UTF-8'))
            client_connection.send('end'.encode('UTF-8'))

        # If the client wants the list of the current directory
        elif header == 'ls':
            client_connection.send(get_current_directory_names(request_body=request_body))

        # If the client wants to make a new user
        elif header == 'New User':
            hashed_password = security.encrypt_password(request_body.get('password'))
            username = request_body.get('username')

            file = open('security/passwords.txt', 'wb')
            file.write((username + '\n' + hashed_password + '\n').encode('UTF-8'))
            file.close()

    client_connection.close()


def get_current_directory_names(request_body):
    dir_file = os.walk(request_body.get('current_directory'))
    dict_of_dict_of_files = {}
    i = 0
    for root, directory, files in dir_file:
        dict_of_files = {
            'current_directory': root,
            'sub_directories': directory,
            'file_names': files,
        }
        dict_of_dict_of_files.update({i: dict_of_files})
        i += 1

    return json.dumps(dict_of_dict_of_files).encode('UTF-8')


def handle_file(request_body, client_connection):
    # Create file path
    directory = os.path.join("C:\\", "Users", "lette", "PycharmProjects", "Python-Socket-Server-Client",
                             request_body.get('directory'))
    print('Directory: ', directory)

    # If the requested directory doesn't exist, create it.
    if not os.path.exists(directory):
        print('Directory: ', directory)
        os.mkdir(directory)

    # Get the file from the client
    sent_file = client_connection.recv(request_body.get('file_size'))
    file_name = os.path.join(directory, request_body.get('file_name'))

    # Write the file to specified location
    file = open(file_name, 'wb')
    file.write(sent_file)
    file.close()


if __name__ == '__main__':
    main()
