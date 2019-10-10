import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = "192.168.0.103"
host = input("Server's ip address and port (exmaple: 192.168.0.100:8000): ").split(':')
s.connect((host[0], int(host[1])))
messages = []

field = []
width, height = 3, 3
for w in range(width):
    line = []
    for h in range(height):
        line.append(' ')
    field.append(line)


def listen():
    messages.append(s.recv(1024).decode())


def send(message):
    s.send(message.encode())


def printfield():
    print("    A  B  C")
    for y in range(len(field[0])):
        fieldline = ' ' + str(y) + ' '
        for x in range(len(field)):
            fieldline += '[' + field[x][y] + ']'
        print(fieldline)


print("Connected, waiting on the other player")
listen()
me = int(messages[0])
if me == 0:
    symbol = 'O'
else:
    symbol = 'X'
print()
print("you're player", symbol)
listen()
turn = messages[1] == "True"
winner = '0'
gameover = False
while not gameover:
    if turn:
        x_move, y_move = 0, 0
        get_move = True
        while get_move:
            print()
            print("It's your turn")
            printfield()
            coordinate = input("Place a " + symbol + " on: ").replace(' ', '')
            x_move = ord(coordinate[0].lower()) - 97
            y_move = int(coordinate[1])
            send(str(x_move))
            time.sleep(0.5)
            send(str(y_move))
            listen()
            if messages[-1] == "illegal move":
                print("Illegal move")
            else:
                get_move = False
                field[x_move][y_move] = symbol
                if not messages[-1] == "move accepted":
                    gameover = True
                    winner = messages[-1]
        turn = False
        printfield()
    else:
        print("It's your oppenent's turn")
        listen()
        opponentsmove = messages[-1].split(':')
        if me == 0:
            field[int(opponentsmove[0])][int(opponentsmove[1])] = 'X'
        else:
            field[int(opponentsmove[0])][int(opponentsmove[1])] = 'O'
        if len(opponentsmove) > 2:
            gameover = True
            winner = opponentsmove[2]
            printfield()
            break
        turn = True

print()
if int(winner) == me:
    print("You won!")
elif int(winner) == -1:
    print("Draw")
else:
    print("You lost.")

time.sleep(1)
send("disconnect")
s.close()
