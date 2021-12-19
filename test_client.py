import socket,re, os
PORT = 9090
from pathlib import Path
HOST = 'localhost'
CURR_DIR = "\\"
sock = ''
MAIN_DIR = Path(os.getcwd(), 'system_home')


def user_msg(login, password, CURR_DIR, msg, c = 0):
    return f"{login}=login, {password}=password, {CURR_DIR}=curr_dir, {c}=len, {msg}=message".encode()

def _send(login, password, CURR_DIR, req):
    global sock, f1, f2
    name = re.split("[ \\/]+", req)[-1]
    curr_path_file = Path(MAIN_DIR, name)
    sock.send(f'send {name}'.encode())
    with open(curr_path_file, 'r') as file:
        text = file.read()
    # sock.send(str(len(text)).encode())
    sock.send(user_msg(login, password, CURR_DIR, text.encode(), len(text)))
    return


def _res(req):
    global sock, f1, f2, MAIN_DIR, CURR_DIR
    flag_finder = sock.recv(1024)
    name = re.split("[ \\/]+", req)[-1]
    print(name)
    length = sock.recv(1024).decode()
    text = sock.recv(len(length)).decode()
    curr_path_file = Path(MAIN_DIR, name)
    with open(curr_path_file, 'w') as file:
        file.write(text)
    return


def main(comm):
    global sock
    login = "tt"
    password = "tt"
    CURR_DIR = login

    sock = socket.socket()
        # req = input(CURR_DIR+'$')
        # print(CURR_DIR, comm)
    req = comm
    req = req.strip()
    if req == 'exit':
        return

    sock.connect((HOST, PORT))
    if req.find("send_from") == 0:
        if req == "send_":
            print("Нет файла")
        else:
            _send(login, password, CURR_DIR, req)

    else:
        sock.send(user_msg(login, password, CURR_DIR, req))
        if req.find("get_to") == 0 or req == "get_to":
            _res(req)
        else:

            response = sock.recv(1024).decode()
            if req.find("cd") == 0:
                if ".." in req:
                    CURR_DIR = login

                            # print(response)
                else:
                    CURR_DIR = response[response.find("\\", response.find(login)):]
            else:
                print(response)


test_comm = [
    "mkdir 21"
    "ls",
    "pwd",
    "dsd"
]

if __name__ == '__main__':

    sock = socket.socket()
    for command in test_comm:
        try:
            main(command)
        except:
            print('Некорректная работа!')
            raise
