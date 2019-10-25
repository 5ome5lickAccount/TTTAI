# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 18:00:02 2019

@author: Christian
"""
from random import randint

total = 0

#This stores a scenario for decision-making purposes
class Decision:

    #The constructor    
    def __init__(self, board, loglocation):
        self.settled = False
        self.coordinates = [-1, -1]
        self.sum = 0
        self.dboard = [[0,0,0],[0,0,0],[0,0,0]]
        self.possibilities = [[0,0,0],[0,0,0],[0,0,0]]
        self.logs = loglocation
        for row in range(3):
            for val in range(3):
                self.dboard[row][val] = board[row][val]
                if (self.dboard[row][val] == 0):
                    self.possibilities[row][val] = 50
                    self.sum = self.sum + 50
    
    #Write data
    def write_data(self, outFile):
        
        #Writes whether or not the current scenario has already been settled, as well as the sum of the possibility grid
        print(self.settled, file=outFile)
        print(self.sum, file=outFile)
        
        #Writes all of the arrays (The board, the possibility grid, and coordinates (Which only matter if the value is settled)
        for row in self.dboard:
            print(row, file=outFile)
        for row in self.possibilities:
            print(row, file=outFile)
        print(self.coordinates, file=outFile)
    
    #Read data
    def read_data(self, inFile):
        
        #Tries to deduct whether or not the specific decision is settled
        placeholder = inFile.readline()
        if (placeholder[0] == "F"):
            self.settled = False
        elif (placeholder[0] == "T"):
            self.settled = True
        
        #Reads the sum
        self.sum = int(inFile.readline())
        
        #This reads the board that it's supposed to remember
        for y in range(3):
            row = inFile.readline()
            self.dboard[y][0] = int(row[1])
            self.dboard[y][1] = int(row[4])
            self.dboard[y][2] = int(row[7])
        
        #This reads the possibility map
        #First though, we need to clear the possibility map
        for y in range(3):
            for x in range(3):
                self.possibilities[y][x] = 0
        
        #Then, we read the map
        for y in range(3):
            num = 0
            row = inFile.readline()
            for i in range((len(row))):
                if (row[i].isdigit()):
                    if ((row[i + 1].isdigit()) and (row[i + 2].isdigit())):
                        self.possibilities[y][num] = self.possibilities[y][num] + (100 * int(row[i]))
                    elif (row[i + 1].isdigit()):
                        self.possibilities[y][num] = self.possibilities[y][num] + (10 * int(row[i]))
                    else:
                        self.possibilities[y][num] = self.possibilities[y][num] + int(row[i])
                        num = num + 1
        
        #Finally, it reads the coordinates, which only matter if the scenario has a decided value
        final = inFile.readline()
        self.coordinates[0] = -2
        self.coordinates[1] = -2
        location = 0
        for i in range((len(final))):
            if (final[i].isdigit()):
                if (final[i - 1] == '-'):
                    self.coordinates[location] = (int(final[i]) * -1)
                else:
                    self.coordinates[location] = int(final[i])
                location = location + 1
        
        #self.write_data(self.logs)
        
        #We recount, just in case
        self.recount()

    #Prints the possibilities being used
    def print_possible(self):
        for row in self.possibilities:
            print(row)
            
    #prints the board
    def print_board(self):
        for row in self.dboard:
            print(row)

    #This decides on a value
    def choose(self):
        if (self.settled == True):
            y = self.coordinates[0]
            x = self.coordinates[1]
            return y, x
        
        #Generates a number between 1 and the sum
        choice = randint(1, self.sum)
        
        #Searches for the value
        for y in range(3):
            for x in range(3):
                choice = choice - self.possibilities[y][x]
                if (choice < 1):
                    return y, x
        
        #If it doesn't work, this just returns bad coordinates to signify that something went wrong
        return -1, -1
    
	#This ensures that the count is accurate, when there is a change
    def recount(self):
        self.sum = 0
        for row in range(3):
            for val in range(3):
                self.sum = self.sum + self.possibilities[row][val]
    
    #The effect of 
    def learn(self, coordinates, result):
        if (self.settled == False):
            y = coordinates[0]
            x = coordinates[1]
            if ((self.possibilities[y][x] + result) < 0):
                self.possibilities[y][x] = 0
                self.recount()
            else:
                self.possibilities[y][x] = self.possibilities[y][x] + result
                self.sum = self.sum + result
            if (self.sum < 1):
                print("A board might be locked up, restarting board")
                for row in range(3):
                    for val in range(3):
                        if (self.dboard[row][val] == 0):
                            self.possibilities[row][val] = 50
                self.recount()
            if (self.possibilities[y][x] > 500):
                self.coordinates[0] = y
                self.coordinates[1] = x
                self.settled = True
                global total
                total = total + 1
                #print(total, file=self.logs)
                #print("Decision board:", file=self.logs)
                #for row in self.dboard:
                    #print(row, file=self.logs)
                #print(x, y, file=self.logs)
            
#This is a potentially bad idea, er, AI.
class TTTAI:
    
    #The constructor
    def __init__(self):
        self.myBoard = [[0,0,0],[0,0,0],[0,0,0]]
        self.size = 1
        self.decisions = []
        self.logs = open("AILogs.py", "w")
        self.decisions.append(Decision(self.myBoard, self.logs))
        self.coordinates = [-1, -1]
        self.locations = []
        self.decidePast = []
        
    #Updates the board as the AI sees it
    def update_board(self, board):
        self.myBoard = board
        
    #Writes data to AIStorage.py
    def write_data(self):
        outFile = open("AIStorage.py", "w")
        print(self.size, file=outFile)
        for i in range(self.size):
            self.decisions[i].write_data(outFile)
        outFile.close()
    
    #Reads data from AIStorage
    def read_data(self):
        inFile = open("AIStorage.py", "r")
        self.decisions = [Decision([[0,0,0],[0,0,0],[0,0,0]], self.logs)]
        self.size = int(inFile.readline())
        self.decisions[0].read_data(inFile)
        for i in range(self.size - 1):
            self.decisions.append(Decision([[0,0,0],[0,0,0],[0,0,0]], self.logs))
            self.decisions[i+1].read_data(inFile)
        print("Finished loading scenarios")
        inFile.close()
    
    #Checks to see if a map and the board match
    def compare(self, num):
        
        #If a single contradiction is found, False is immediately returned
        for y in range(3):
            for x in range(3):
                if (self.decisions[num].dboard[y][x] != self.myBoard[y][x]):
                    return False
        
        #If there were no problems found, True is returned
        return True
    
    def check_maps(self):
        
        #First, this checks every map
        for num in range(self.size):
            if (self.compare(num) == True):
                return num
        
        #Since a matching map isn't found (If the code reaches this point) it makes a new one
        self.decisions.append(Decision(self.myBoard, self.logs))
        self.size = self.size + 1
        return (self.size - 1)
    
    #This function takes a turn using decisions it knows, or the ones it creates on the spot
    def take_turn(self):
        
        #Checks for any maps which match the current scenario
        decide = self.check_maps()
        
        #This returns x and y coordinates
        y, x = self.decisions[decide].choose()
        
        #Checks to see if something went wrong
        if (y == -1):
            print("Something went wrong during the decision-making process")
            return -2, -2
            
        if (self.myBoard[y][x] > 0):
            print("Um...This wants to take a filled spot.")
            print("x:", x, "y:", y)
            print("Probability map:", self.decisions[decide].possibilities)
            print("The map for decision making:")
            self.decisions[decide].print_board()
            print(self.myBoard)
            print(self.decisions[decide].settled)
            print('\n')
            return -1, -1
        
        #Otherwise, things proceed as planned
        self.coordinates[0] = y
        self.coordinates[1] = x
        self.locations.append([y, x])
        self.decidePast.append(decide)
        
        #returns coordinates
        return y, x
    
    #This makes the move for three arrays
    def three_list_move(self, a, b, c):
        for i in range(3):
            self.myBoard[0][i] = a[i]
            self.myBoard[1][i] = b[i]
            self.myBoard[2][i] = c[i]
        
        y, x = self.take_turn()
        if (y == 0):
            a[x] = 2
        elif (y == 1):
            b[x] = 2
        elif (y == 2):
            c[x] = 2
        else:
            print("Something went wrong while trying to make a move...")
    
    #This resets everything relevant to a game
    def new_game(self):
        self.decidePast = []
        self.locations = []
        self.myBoard = [[0,0,0],[0,0,0],[0,0,0]]
    
    #This is where the AI's biggest strength comes into play: learning
    def teach(self, win, stale):

        #print(self.locations, file=self.logs)
        
        #Figures out how many times maps were used, then teaches the used maps
        times = len(self.decidePast)
        for val in range(times):
            
            #If the game was won, we reward the decision. Otherwise, we punish it
            if (stale == True):
                #self.decisions[self.decidePast[val]].learn(self.locations[val], -1)
                return 0
            else:
                if (win == True):
                    #self.decisions[self.decidePast[val]].learn(self.locations[val], int((val + 1) * 1))
                    self.decisions[self.decidePast[val]].learn(self.locations[val], 5)
                else:
                    #self.decisions[self.decidePast[val]].learn(self.locations[val], int((0 - (val + 1)) * 1))
                    self.decisions[self.decidePast[val]].learn(self.locations[val], -5)


"""
The main TicTacToe program which I made
"""


#Checks to see if a player has won, returns the player number 
def check_win(board):
    if board[0][0] == board[1][0] and board[0][0] == board[2][0] and board[0][0] > 0:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[0][1] == board[2][1] and board[0][1] > 0:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[0][2] == board[2][2] and board[0][2] > 0:
        return board[0][2]
    elif board[0][0] == board[0][1] and board[0][0] == board[0][2] and board[0][0] > 0:
        return board[0][0]
    elif board[1][0] == board[1][1] and board[1][0] == board[1][2] and board[1][0] > 0:
        return board[1][0]
    elif board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] > 0:
        return board[2][0]
    elif board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[1][1] > 0:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[1][1] > 0:
        return board[0][2]
    return 0

#Checks for stalemates
def check_stale(board):
    for row in board:
        for val in row:
            if val == 0:
                return 0
    return 1

#This prints the current board into it's tic-tac-toe form (Rather than lists within a list)
def print_board(board):
    print("\n")
    print("  ", 1, "" , 2, "", 3)
    for row in range(3):
        print(row + 1, board[row])

#A random part of the board is selected
def rand_ai_move(board):
    times = 0
    for row in range(3):
        for val in range(3):
            if (board[row][val] == 0):
                times = times + 1
    move = randint(1, times)
    for row in range(3):
        for val in range(3):
            if (board[row][val] == 0):
                move = move - 1
                if (move < 1):
                    board[row][val] = 2
                    return 0

#The opportunist is a trainer AI which wins if it can. Otherwise, it will use a random move
def opportunist(board):
    
    if (board[0][0] + board[0][1] + board[0][2] == 4 and (board[0][0] == 0 or board[0][1] == 0 or board[0][2] == 0)):
        if (board[0][0] == 0):
            board[0][0] = 2
        elif (board[0][1] == 0):
            board[0][1] = 2
        elif (board[0][2] == 0):
            board[0][2] = 2
        else:
            print("1 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[1][0] + board[1][1] + board[1][2] == 4 and (board[1][0] == 0 or board[1][1] == 0 or board[1][2] == 0)):
        if (board[1][0] == 0):
            board[1][0] = 2
        elif (board[1][1] == 0):
            board[1][1] = 2
        elif (board[1][2] == 0):
            board[1][2] = 2
        else:
            print("2 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[2][0] + board[2][1] + board[2][2] == 4 and (board[2][0] == 0 or board[2][1] == 0 or board[2][2] == 0)):
        if (board[2][0] == 0):
            board[2][0] = 2
        elif (board[2][1] == 0):
            board[2][1] = 2
        elif (board[2][2] == 0):
            board[2][2] = 2
        else:
            print("3 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[0][0] + board[1][0] + board[2][0] == 4 and (board[0][0] == 0 or board[1][0] == 0 or board[2][0] == 0)):
        if (board[0][0] == 0):
            board[0][0] = 2
        elif (board[1][0] == 0):
            board[1][0] = 2
        elif (board[2][0] == 0):
            board[2][0] = 2
        else:
            print("4 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[0][1] + board[1][1] + board[2][1] == 4 and (board[0][1] == 0 or board[1][1] == 0 or board[2][1] == 0)):
        if (board[0][1] == 0):
            board[0][1] = 2
        elif (board[1][1] == 0):
            board[1][1] = 2
        elif (board[2][1] == 0):
            board[2][1] = 2
        else:
            print("5 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[0][2] + board[1][2] + board[2][2] == 4 and (board[0][2] == 0 or board[1][2] == 0 or board[2][2] == 0)):
        if (board[0][2] == 0):
            board[0][2] = 2
        elif (board[1][2] == 0):
            board[1][2] = 2
        elif (board[2][2] == 0):
            board[2][2] = 2
        else:
            print("6 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[0][0] + board[1][1] + board[2][2] == 4 and (board[0][0] == 0 or board[1][1] == 0 or board[2][2] == 0)):
        if (board[0][0] == 0):
            board[0][0] = 2
        elif (board[1][1] == 0):
            board[1][1] = 2
        elif (board[2][2] == 0):
            board[2][2] = 2
        else:
            print("7 went wrong")
            rand_ai_move(board)
        return 0
    
    elif (board[2][0] + board[1][1] + board[0][2] == 4 and (board[2][0] == 0 or board[1][1] == 0 or board[0][2] == 0)):
        if (board[2][0] == 0):
            board[2][0] = 2
        elif (board[1][1] == 0):
            board[1][1] = 2
        elif (board[0][2] == 0):
            board[0][2] = 2
        else:
            print("8 went wrong")
            rand_ai_move(board)
        return 0
    
    rand_ai_move(board)

#This is where a user makes a move
def player_move(board, current):
    move = False
    while move == False:
        x = int(input("x value? (1, 2, or 3) "))
        y = int(input("y value? (1, 2, or 3) "))
        if (board[(y - 1)][(x - 1)] > 0):
            print("The spot you wish to claim has already been taken.\n")
        else:
            move = True
    board[(y - 1)][(x - 1)] = current

#Makes sure that the outcome is either a victory or a loss
def check_end(board):
    check = check_win(board)
    if (check > 0):
        return check
    else:
        if (check_stale(board) == 0):
            return 0
        else:
            return 3

#This is a pvp game between two players
def pvp_game():
    board = [[0,0,0],[0,0,0],[0,0,0]]
    current = int(input("Who goes first? 1 or 2? "))
    check = 0
    print_board(board)
    while current < 3:
        player_move(board, current)
        print_board(board)
        check = check_end(board)
        if (check == 0):
            if (current == 1):
                current = 2
            else:
                current = 1
        elif (check < 3):
            print(check, "won! Press 1 for a rematch")
            current = int(input())
            if (current == 1):
                pvp_game()
            return 0
        else:
            current = int(input("Stalemate. Press 1 for a rematch"))
            if (current == 1):
                pvp_game()
            return 0

#This is a player verses random ai game
def rand_game():
    board = [[0,0,0],[0,0,0],[0,0,0]]
    current = int(input("Who goes first? 1 or 2? "))
    check = 0
    print_board(board)
    while current < 3:
        if (current == 1):
            player_move(board, 1)
        else:
            rand_ai_move(board)
            #opportunist(board)
        print_board(board)
        check = check_end(board)
        if (check == 0):
            if (current == 1):
                current = 2
            else:
                current = 1
        elif (check < 3):
            print(check, "won! Press 1 for a rematch")
            current = int(input())
            if (current == 1):
                rand_game()
            return 0
        else:
            current = int(input("Stalemate. Press 1 for a rematch"))
            if (current == 1):
                rand_game()
            return 0

#This is where a player faces off with THE ai
def ai_game(AI):
    board = [[0,0,0],[0,0,0],[0,0,0]]
    current = int(input("Who goes first? 1 or 2? "))
    check = 0
    print_board(board)
    while current < 3:
        if (current == 1):
            player_move(board, 1)
        else:
            AI.update_board(board)
            y, x = AI.take_turn()
            board[y][x] = 2
        print_board(board)
        check = check_end(board)
        if (check == 0):
            if (current == 1):
                current = 2
            else:
                current = 1
        elif (check < 3):
            print(check, "won! Press 1 for a rematch")
            current = int(input())
            if (current == 1):
                ai_game(AI)
            return 0
        else:
            current = int(input("Stalemate. Press 1 for a rematch"))
            if (current == 1):
                ai_game(AI)
            return 0
    
#This is where the training and leraning begins    
def training(AI):
    
    #Gathers information
    times = int(input("How many times will the AI be tested? "))
    learn = int(input("Will the AI learn? 1 for yes, any other int for no "))
    first = 1
    result = 0
    results = []
    won = 0
    lost = 0
    draw = 0
    
    #Then, begins the challenge
    for i in range(times):
        AI.new_game()
        result = arena(AI, first)
        if (result == 1):
            won = won + 1
        elif (result == 2):
            lost = lost + 1
        else:
            draw = draw + 1
        if (learn == 1):
            if (result == 1):
                AI.teach(True, False)
            elif (result == 2):
                AI.teach(False, False)
            else:
                AI.teach(False, True)
        if (first == 1):
            first = 2
        else:
            first = 1
        results.append(result)
        if ((i + 1) % 1000 == 0):
            print(i + 1)
    
    print("Won:", won, "\nLost", lost, "\nDraw:", draw)
    print("\nTotal decision maps:", AI.size)
    print("Total settled values:", total)
    return 0

#This is the arena where a random AI faces off with the learning AI
def arena(AI, first):
    board = [[0,0,0],[0,0,0],[0,0,0]]
    current = first
    check = 0
    while current < 3:
        if (current == 1):
            AI.update_board(board)
            y, x = AI.take_turn()
            if (y == -2):
                print_board(board)
            board[y][x] = 1
        else:
            opportunist(board)
        check = check_end(board)
        if (check == 0):
            if (current == 1):
                current = 2
            else:
                current = 1
        elif (check < 3):
            #print_board(board)
            return check
        else:
            #print_board(board)
            return 3
    
#This is just for organization sake. I don't like to see a lot of print statements by the main menu
def print_menu():
    print("1 - Play against another player")
    print("2 - Play against a random AI")
    print("3 - Test the three_list_move function")
    print("4 - Play against the, potentially catastrophic, learning AI")
    print("5 - Load the contents of AIStorage.py into the learning AI")
    print("6 - Write the contents of the learning AI into AIStorage.py")
    print("7 - Train the learning AI")
    print("Any other int - Exit the program", '\n')

#This one runs everything, basically
def main():
    underling = TTTAI()
    print("Welcome to TTTAI.py version 0.9, what do you want?")
    while(True):
        print_menu()
        val = input()
        if (val.isdigit()):
            val = int(val)
            if (val == 1):
                pvp_game()
            elif (val == 2):
                rand_game()
            elif (val == 3):
                a = [1,1,2]
                b = [2,0,2]
                c = [2,1,1]
                underling.three_list_move(a, b, c)
                print(a)
                print(b)
                print(c)
            elif (val == 4):
                ai_game(underling)
            elif (val == 5):
                try:
                    underling.read_data()
                except:
                    print("Something went wrong while trying to load the proper data")
            elif (val == 6):
                underling.write_data()
            elif (val == 7):
                training(underling)
            elif (val == 100):
                outFile = open("AILogs.py", "w")
                print("Preparing to write data to the outFile...")
                for i in range(underling.size):
                    underling.decisions[i].write_data(outFile)
                if (underling.size > 1):
                    underling.decisions[1].print_board()
                    underling.decisions[1].print_possible()
                    print(underling.decisions[1].coordinates)
                else:
                    underling.decisions[0].print_board()
                    underling.decisions[0].print_possible()
                    print(underling.decisions[0].coordinates)
                outFile.close()
            else:
                underling.logs.close()
                return 0
    return 0

main()