from socket import *
from time import *
import pickle
from inputimeout import inputimeout
from tabulate import tabulate

columns1 = ["Players", "Cumulative Scores"]  # for printing the tables #Jennifer and Charbel
columns2 = ["Players", "Final Scores"]#Jennifer and Charbel
count = 0 # Don Carlos and Wael
port = 12000 # Don Carlos and Wael

try:
    client = socket(AF_INET, SOCK_STREAM) # Don Carlos and Wael
    client.connect((gethostname(), port))  # trying to connect to server # Don Carlos and Wael
except:
    print("You were unable to join!")  # if server has stopped accpeting connections... # Don Carlos and Wael
    exit()

print(client.recv(1024).decode())  # Receiving welcome message # Don Carlos and Wael
for i in range(3):
    x = client.recv(1024).decode()  # Receiving number # Don Carlos and Wael
    try:
        n = inputimeout(f"Enter {x}: ",5)  # this special input allows the user to input with a 5 second limit, shall he exceed that, the player disconnects # Don Carlos and Wael
        # and the game is declared over

        if n == "":  # this is to treat the case when the client presses enter without any input #Wael
            n = "-1"
    except:
        print("You have been disconnected, be quick !")  # player takes too much time to enter the number... #Don Carlos, wording by Jennifer and Charbel
        client.close()
        break
    client.send(n.encode())
    l = client.recv(4096)  # Receiving one of 2 things, either an array beginning with quit signaling that one of the player has disconnected #Wael
    res = pickle.loads(l)  # loading the array # Wael
    if res[0] == 'quit':  # checking if the array is the disconnected array
        res.remove('quit') #Don Carlos
        res = list(set(res)) #Don Carlos
        if len(res) > 1: #Charbel and Jennifer
            s = ""
            for p in res: s += f" {p},"  # checking which players have disconnected
            print(f"Game Over, Players" + s[:-1] + " have disconnected!")  # removing last , and printing #Charbel
        else:
            print(
                f"Game Over, Player {res[0]} has disconnected!")  # else only one player has disconnected, print that player, in the case above, multiple have disconnected
            #Wael and Don Carlos
        break
    c = client.recv(4096)  # this receive is for the cumulative scores #Wael and Don Carlos
    cumu = pickle.loads(c) #Wael and Don Carlos
    print("\nROUND " + str(i + 1) + ': ') #Jennifer and Charbel
    for x in res:
        print(*x) #Don Carlos
    if i != 2:
        print(tabulate(cumu, headers=columns1, tablefmt="fancy_grid"))#Jennifer and Charbel
        print()

    if i == 2:
        print(tabulate(cumu, headers=columns2, tablefmt="fancy_grid")) #Jennifer and Charbel
        maxi = cumu[0][1]
        tie = [cumu[0][0]]
        for i in range(1, len(cumu)):
            if cumu[i][1] != maxi: break #Don Carlos and Wael
            tie.append(cumu[i][0])
        if len(tie) > 1:
            print("It's a tie between players: ", end=" ") #Wael and Don Carlos
            for p in range(len(tie)):
                if p != len(tie) - 1:
                    print(str(tie[p]), ',', end=" ")
                else:
                    print(tie[p])
        else:
            print("Player " + str(tie[0]) + " won ! ") #Jennifer and Charbel
        # the above chunk of code is to determine whether we have a tie or not.
        # lines 44->52 : printing scores and checking if last round to print final results.

# Charbel and Jennifer contributed to the format/layout of the game and what should happen if
# specific situations happen game wise (score distribution, disconnection,...)

# Don Carlos and Wael contributed to designing the communication between the server and clients and error
# handling from both hides

# gDesign: tabulation, layout of text (display format...)
# communication: error handling, sending and receiving protocols,timeouts...
# We all contributed in debugging the code several times in order to find errors in the code