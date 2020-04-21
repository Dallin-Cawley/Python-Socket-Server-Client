import os
import socket
from pip._vendor.distlib.compat import raw_input
import json
import tkinter

user = ""
login_success = False
client_socket = socket.socket()


def main():
    global login_success
    main_window = tkinter.Tk()
    main_window.geometry('750x400')
    main_window.resizable(False, False)

    login_canvas = tkinter.Canvas(main_window, width='750', height='400')
    login_canvas.pack()

    username_label = tkinter.Label(main_window, text="Username:")
    login_canvas.create_window(340, 155, window=username_label)

    username_input = tkinter.Entry(main_window)
    login_canvas.create_window(375, 175, window=username_input)

    password_label = tkinter.Label(main_window, text="Password:")
    login_canvas.create_window(340, 200, window=password_label)

    password_input = tkinter.Entry(main_window)
    login_canvas.create_window(375, 225, window=password_input)

    entry_boxes = {
        'username': username_input,
        'password': password_input
    }

    login_button = tkinter.Button(text='Submit', command=lambda: login(entry_boxes=entry_boxes))
    login_canvas.create_window(385, 250, window=login_button)

    main_window.mainloop()

    while True:
        if login_success:
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
                    print(json.loads(client_socket.recv(1024).decode('UTF-8')).get('response'))
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


def login(entry_boxes):
    global login_success
    global user
    global client_socket
    print('inside login()\n')
    body = {
        'header': 'login',
        'username': entry_boxes.get('username').get(),
        'password': entry_boxes.get('password').get()
    }

    # Connect to remote host
    client_socket.connect((socket.gethostname(), 8001))
    print(json.loads(client_socket.recv(1024).decode('UTF-8')).get('response'), '\n')

    client_socket.sendall(json.dumps(body).encode('UTF-8'))
    response = json.loads(client_socket.recv(1024).decode('UTF-8'))

    if response.get('response') == 'true':
        user = response.get('user')
        login_success = True
        return True, client_socket
    else:
        return False, False


def send_file(client_socket, file_name):
    try:
        file_path = os.path.abspath(file_name)
        file_size = os.path.getsize(file_path)

        body = {
            'header': 'file',
            'file_type': os.path.splitext(file_path)[1],
            'file_name': os.path.basename(file_path),
            'file_size': file_size,
            'directory': user

        }

        file = open(file_path, 'rb')

        file_bytes = file.read(file_size)
        file.close()

        client_socket.sendall(json.dumps(body).encode('UTF-8'))
        client_socket.sendall(file_bytes)

        print(json.loads(client_socket.recv(1024).decode('UTF-8')).get('response'))
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
