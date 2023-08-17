from socket import *
from time import *
from random import *
import pickle
from tabulate import tabulate

port = 12000 
server = socket(AF_INET, SOCK_STREAM)  # Creating socket 
server.bind((gethostname(), port))
server.listen(100)
print("Ready to recieve")
print("Waiting for players to join")
clients = []  # List to store all client connections 

server.settimeout(10)  # 10 seconds for all players to join 
count = 1 

try:
    while True:
        client, add = server.accept()  # Accepting connections 
        client.settimeout(5)  # This means that if a response is not received within a certain amount of time ( 5 seconds) , the socket will give up waiting and raise an exception.
        clients.append(client)  # Appending the new client to our list 
        client.send(f"Welcome, you are player {count}!".encode()) 
        print(f"Connection Established with player {count} from address {add}") 
        count += 1  # incrementing the number of players 
except:
    print(f"Number of players: {count - 1}")  # Timeout has occured, server has stopped accepting new players 
    server.close()

numofplayers = count - 1 

columns1 = ["Players", "Cumulative Scores"]  # for printing the tables 
columns2 = ["Players", "Final Scores"] 

while True:
    cumu = []  # List of cumulative scores, to be filled 
    discon = ['quit']  # This is used later to tell other players if a player has disconnected or not 

    if numofplayers == 0:  # if no players join the game 
        break 

    for i in range(0, numofplayers): 
        cumu.append([i + 1, 0])  # Initializing cumulative score array to 0's 
    for i in range(3):
        bools = False; 
        disc = -1 
        x = randint(0, 9)  # Generating random number between 0 and 9 inclusive 
        temp = [] 

        for j in range(1, numofplayers + 1): 
            temp.append([j, float('inf')])  # Initializing temp array to keep track of current round scores
        player = 0
        for client in clients: 
            sleep(0.5) 
            st = time()  # Time of sending number
            try:
                client.send(str(x).encode())  # Try to send number to client
            except:
                bools = True;  # if unable to send, the player has an issue with his connection, ie has disconnected so we should end the game
                discon.append(player + 1)  # this list is used to keep track of disconnected players, we handled the case of displaying multiple player disconnections
            try:
                ans = client.recv(1024).decode()  # same idea as sending
            except:
                bools = True;
                discon.append(player + 1)
            end = time()
            if not bools:
                if (str(ans) == str(x)):
                    temp[player][1] = end - st  # if no disconnection, compare player's answer to the number sent, if they match, find the rtt and store it int the temp array
            player += 1
        if bools:
            for p in range(numofplayers):
                if (p + 1 not in discon):
                    clients[p].send(pickle.dumps(discon))  # if there is a disconnection, we need to send to all other players this array which starts with 'quit'
                    # upon receiving this array the clients will check if the first element is 'quit' to tell if the game is going or not
                    # in case the game should end, the list also contains the players that have disconnected
            break  # terminate all rounds in case the game is over

        temp.sort(key=lambda x: x[1])  # if the game has not ended, sort the game based on rtt's #Idea by everyone 82->86
        for j in range(len(temp)):
            if (temp[j][1] != float('inf')):  # if the rtt of a player is not inf meaning that he entered the correct number,
                # then the player should get an increment of his score, which we decided to be the number of players - (his position in the current round-1)
                cumu[temp[j][0] - 1][1] += (numofplayers - j)  # here we add each score to the cumulative score array

        res = []
        a = numofplayers 
        for j in range(len(temp)): 
            if temp[j][1] == float('inf'): 
                a = j
                break
            res.append([str(j + 1) + ") Player " + str(temp[j][0])]) 
        if a != numofplayers:
            temp2 = ["Wrong answers:"]
            for j in range(a, numofplayers):
                if j != numofplayers - 1:
                    temp2.append("Player " + str(temp[j][0]) + ',')
                else:
                    temp2.append("Player " + str(temp[j][0]))
            # Lines 81 to 94 check the players that have entered a wrong number to declare that later on
            res.append(temp2)
        print("\nROUND " + str(i + 1) + ': ')
        for x in res:
            print(*x) 
        for a in clients:
            a.send(pickle.dumps(res)) 
        # sending results of each round to the players
        cumu.sort(key=lambda x: x[1], reverse=True)  # sorting cumulative score array #Everyone contributed from 110-> 119
        sleep(0.1)
        for a in clients:
            a.send(pickle.dumps(cumu))
        if (i != 2):
            print(tabulate(cumu, headers=columns1, tablefmt="fancy_grid"))
            print()
        # sending results of each round to the players

        cumu.sort(key=lambda x: x[0], reverse=False)  # return to initial state to fill up later on
    # in the following lines we print the final scores

    if not bools and numofplayers != 0:
        cumu.sort(key=lambda x: x[1], reverse=True)
        print(tabulate(cumu, headers=columns2, tablefmt="fancy_grid"))
        maxi = cumu[0][1]
        tie = [cumu[0][0]]
        for i in range(1, numofplayers):
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
        # the above chunk of code is to determine whether we have a tie or not.
    break

# Design: tabulation, layout of text (display format...)
# Communication: error handling, sending and receiving protocols,timeouts...

# We all contributed in debugging the code several times in order to find errors in the code
