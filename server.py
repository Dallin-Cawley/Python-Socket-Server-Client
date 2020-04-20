import socket
from _thread import *
from pip._vendor.distlib.compat import raw_input
import json
import RequestHandler
import globals


def main():
    globals.init()
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
    # Load user's info for authentication
    users_file = open('security/passwords.txt', 'r')
    globals.users = json.loads(str(users_file.read()))

    # Accept an incoming connection
    while True:
        connection, con_address = server_socket.accept()
        start_new_thread(handle_client_connection, (connection,))


def handle_client_connection(client_connection):
    # Handle the connection
    body = {
        'response': 'Connection Accepted'
    }
    client_connection.sendall(json.dumps(body).encode('UTF-8'))
    request_handler = RequestHandler.RequestHandlerSwitch()
    while True:
        data = client_connection.recv(1024)
        request_body = json.loads(data)
        request_body.update({'client_connection': client_connection})
        header = request_body.get('header')

        # When the Client wishes to disconnect
        if header == 'quit':
            body = {
                'response': 'Connection Terminating'
            }
            client_connection.sendall(json.dumps(body).encode('UTF-8'))
            break

        client_connection.sendall(request_handler.handle_request(header=header, request_body=request_body))

    client_connection.close()


if __name__ == '__main__':
    main()
