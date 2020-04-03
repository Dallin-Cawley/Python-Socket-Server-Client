import socket
from _thread import *
from pip._vendor.distlib.compat import raw_input


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
    while True:

        if data.decode('UTF=8') == 'quit':
            response_data = 'Connection Terminating'
            client_connection.send(response_data.encode('UTF8'))
            break

        response_data = "You sent: " + str(data)
        client_connection.send(response_data.encode('UTF-8'))
        data = client_connection.recv(1024)

    client_connection.close()


if __name__ == '__main__':
    main()
