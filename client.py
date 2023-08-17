from socket import *
from time import *
import pickle
from inputimeout import inputimeout
from tabulate import tabulate

columns1 = ["Players", "Cumulative Scores"]  # for printing the tables
columns2 = ["Players", "Final Scores"]
count = 0
port = 12000

try:
    client = socket(AF_INET, SOCK_STREAM) 
    client.connect((gethostname(), port))  # trying to connect to server 
except:
    print("You were unable to join!")  # if server has stopped accpeting connections... 
    exit()

print(client.recv(1024).decode())  # Receiving welcome message 
for i in range(3):
    x = client.recv(1024).decode()  # Receiving number 
    try:
        n = inputimeout(f"Enter {x}: ",5)  # this special input allows the user to input with a 5 second limit, shall he exceed that, the player disconnects 
        # and the game is declared over

        if n == "":  # this is to treat the case when the client presses enter without any input
            n = "-1"
    except:
        print("You have been disconnected, be quick !")  # player takes too much time to enter the number...
        client.close()
        break
    client.send(n.encode())
    l = client.recv(4096)  # Receiving one of 2 things, either an array beginning with quit signaling that one of the player has disconnected
    res = pickle.loads(l)  # loading the array
    if res[0] == 'quit':  # checking if the array is the disconnected array
        res.remove('quit')
        res = list(set(res))
        if len(res) > 1: 
            s = ""
            for p in res: s += f" {p},"  # checking which players have disconnected
            print(f"Game Over, Players" + s[:-1] + " have disconnected!")  # removing last , and printing
        else:
            print(
                f"Game Over, Player {res[0]} has disconnected!")  # else only one player has disconnected, print that player, in the case above, multiple have disconnected
        break
    c = client.recv(4096)  # this receive is for the cumulative scores
    cumu = pickle.loads(c) 
    print("\nROUND " + str(i + 1) + ': ') 
    for x in res:
        print(*x)
    if i != 2:
        print(tabulate(cumu, headers=columns1, tablefmt="fancy_grid"))
        print()

    if i == 2:
        print(tabulate(cumu, headers=columns2, tablefmt="fancy_grid"))
        maxi = cumu[0][1]
        tie = [cumu[0][0]]
        for i in range(1, len(cumu)):
            if cumu[i][1] != maxi: break
            tie.append(cumu[i][0])
        if len(tie) > 1:
            print("It's a tie between players: ", end=" ")
            for p in range(len(tie)):
                if p != len(tie) - 1:
                    print(str(tie[p]), ',', end=" ")
                else:
                    print(tie[p])
        else:
            print("Player " + str(tie[0]) + " won ! ")
        # the above chunk of code is to determine whether we have a tie or not.
        # lines 44->52 : printing scores and checking if last round to print final results.
