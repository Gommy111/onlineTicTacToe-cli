import random
import socket
import time
from threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = "192.168.0.103"
host = input("Server's ip address and port (exmaple: 192.168.0.100:8000): ").split(':')
serversocket.bind((host[0], int(host[1])))

field = []
width, height = 3, 3
for w in range(width):
    line = []
    for h in range(height):
        line.append(' ')
    field.append(line)


def printfield():
    for y in range(len(field[0])):
        fieldline = ""
        for x in range(len(field)):
            fieldline += '[' + field[x][y] + ']'
        print(fieldline)


def num_smb(number):
    if number == 0:
        return 'O'
    return 'X'


class Client(Thread):
    def __init__(self, csocket, caddress):
        Thread.__init__(self)
        self.sock = csocket
        self.addr = caddress
        self.messages = ['test']
        self.disconnected = False
        self.start()

    def get_messages(self):
        return self.messages

    def send_message(self, message):
        message = message.encode()
        self.sock.send(message)

    def run(self):
        while not self.disconnected:
            message = self.sock.recv(1024).decode()
            if len(message) > 0:
                print(self.addr[0], 'sent:', message)
                if message == "disconnect":
                    self.disconnected = True
                    break
                self.messages.append(message)
                # self.sock.send(b'recieved')


serversocket.listen(2)
clients = []
print('server started and listening')
for i in range(2):
    clientsocket, address = serversocket.accept()
    print(address[0], "connected")
    clients.append(Client(clientsocket, address))
print(clients)
turn = random.randint(0, len(clients) - 1)
print(turn)
for i in range(len(clients)):
    clients[i].send_message(str(i))

time.sleep(0.5)
for c in range(len(clients)):
    clients[c].send_message(str(c == turn))
gameover = False
while not gameover:
    x_move, y_move = 0, 0
    get_move = True
    while get_move:
        old_msg_length = len(clients[turn].get_messages())
        while len(clients[turn].get_messages()) <= old_msg_length + 1:
            time.sleep(0.1)
        x_move = int(clients[turn].get_messages()[-2])
        y_move = int(clients[turn].get_messages()[-1])
        if 0 <= x_move < len(field) and 0 <= y_move < len(field[0]):
            if field[x_move][y_move] == ' ':
                get_move = False
            else:
                clients[turn].send_message("illegal move")
        else:
            clients[turn].send_message("illegal move")
    field[x_move][y_move] = num_smb(turn)
    printfield()

    for chSy in range(2):
        gameover = (field[0][0] == num_smb(chSy) and field[1][0] == num_smb(chSy) and field[2][
            0] == num_smb(chSy)) or \
                   (field[0][1] == num_smb(chSy) and field[1][1] == num_smb(chSy) and field[2][
                       1] == num_smb(chSy)) or \
                   (field[0][2] == num_smb(chSy) and field[1][2] == num_smb(chSy) and field[2][
                       2] == num_smb(chSy)) or \
                   (field[0][0] == num_smb(chSy) and field[0][1] == num_smb(chSy) and field[0][
                       2] == num_smb(chSy)) or \
                   (field[1][0] == num_smb(chSy) and field[1][1] == num_smb(chSy) and field[1][
                       2] == num_smb(chSy)) or \
                   (field[2][0] == num_smb(chSy) and field[2][1] == num_smb(chSy) and field[2][
                       2] == num_smb(chSy)) or \
                   (field[0][0] == num_smb(chSy) and field[1][1] == num_smb(chSy) and field[2][
                       2] == num_smb(chSy)) or \
                   (field[0][2] == num_smb(chSy) and field[1][1] == num_smb(chSy) and field[2][
                       0] == num_smb(chSy))
        if gameover:
            winner = chSy
            break
    impossible = False
    for y in range(len(field)):
        for x in range(len(field[0])):
            impossible = impossible or field[x][y] == ' '
    if not impossible:
        gameover = True
        winner = -1
    if gameover:
        clients[turn].send_message(str(winner))
    else:
        clients[turn].send_message("move accepted")

    if turn == 0:
        turn = 1
    else:
        turn = 0
    if gameover:
        clients[turn].send_message(str(x_move) + ':' + str(y_move) + ':' + str(winner))
        print("GAME OVER")
        if(int(winner) == -1):
            print("Draw")
        else:
            print(num_smb(winner), "won")
    else:
        clients[turn].send_message(str(x_move) + ':' + str(y_move))
