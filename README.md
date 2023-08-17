# Fastest Finger First (Delay Multiplayer Game)
## Overview
This is a networked multiplayer game where players compete to respond the fastest to random numbers sent by the server. The fastest player to enter the correct number wins the round. Players gain points based on how fast they respond compared to other players. The game lasts 3 rounds. The player with the highest cumulative score at the end wins.

### How to Play

- The server needs to be started first to accept connections
- Players then connect to the server as clients
- Once enough players have joined, the game begins
- Each round:
  - The server sends a random number to each client
  - Clients enter the number as fast as they can
  - The fastest player to enter the correct number wins the round
  - Players are ranked based on response time
  - Points are awarded based on rank
  - Cumulative scores are updated
- After 3 rounds, the player with the highest cumulative score wins

### Features

- Multiplayer game with client/server model
- Random number generation
- Timing and scoring based on response speed
- Cumulative score tracking
- Table printing of scores and results
- Disconnection handling and game termination
- Timeout on client number input

## Code Structure

### Server

- Initializes socket and accepts client connections
- Manages game state
- Sends random numbers to clients
- Receives responses from clients
- Tracks round timing and scores
- Prints round and game results
- Handles disconnections

### Client

- Connects to server
- Receives random numbers
- Inputs number response
- Prints round and cumulative scores
- Handles disconnection from server
- Times out if response takes too long

### Technologies

- Python
- Sockets for networking
- Pickling for sending data between client and server
- Tabulate for printing tables
- Timeouts and exception handling for disconnections
