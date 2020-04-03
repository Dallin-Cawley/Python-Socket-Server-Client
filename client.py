import socket
from pip._vendor.distlib.compat import raw_input


def main():
    # Create a socket
    client_socket = socket.socket()

    # Connect to remote host
    client_socket.connect((socket.gethostname(), 2222))

    # Send some information to the host.
    user_input = raw_input("Send to host: ")

    while True:
        client_socket.send(user_input.encode('UTF-8'))
        print(client_socket.recv(1024).decode('UTF-8'), '\n')

        if user_input == 'quit':
            break

        user_input = raw_input("Send to host: ")


if __name__ == '__main__':
    main()
