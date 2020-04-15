import socket
from _thread import *
from pip._vendor.distlib.compat import raw_input
import json


def main():
    # Create a socket
    server_socket = socket.socket()

    # Bind the socket to a port for use
    server_socket.bind((socket.gethostname(), 2222))

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

        if request_body.get('header') == 'quit':
            response_data = 'Connection Terminating'
            client_connection.send(response_data.encode('UTF8'))
            break

        if request_body.get('header') == 'file':
            file = open('files-recieved/' + request_body.get('file_name'), 'wb')
            sent_file = client_connection.recv(request_body.get('file_size'))
            file.write(sent_file)
            file.close()
            client_connection.send('File saved'.encode('UTF-8'))

        elif request_body.get('header') == 'message':
            client_connection.send(('You sent: ' + request_body.get('message')).encode('UTF-8'))
            client_connection.send('end'.encode('UTF-8'))

    client_connection.close()


if __name__ == '__main__':
    main()
