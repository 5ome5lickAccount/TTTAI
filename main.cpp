#include <string>
#include <iostream>
#include <fstream>
#include <time.h>
#include "TTTAI.h"



//Checks to see if a player has won
int CheckWin(int board[3][3]) {

	//...Yup. All of the branching statements
	if (board[0][0] == board[0][1] && board[0][0] == board[0][2] && board[0][0] > 0) {
		return board[0][0];
	} else if (board[1][0] == board[1][1] && board[1][0] == board[1][2] && board[1][0] > 0) {
		return board[1][0];
	} else if (board[2][0] == board[2][1] && board[2][0] == board[2][2] && board[2][0] > 0) {
		return board[2][0];
	} else if (board[0][0] == board[1][0] && board[0][0] == board[2][0] && board[0][0] > 0) {
		return board[0][0];
	} else if (board[0][1] == board[1][1] && board[0][1] == board[2][1] && board[0][1] > 0) {
		return board[0][1];
	} else if (board[0][2] == board[1][2] && board[0][2] == board[2][2] && board[0][2] > 0) {
		return board[0][2];
	} else if (board[0][0] == board[1][1] && board[0][0] == board[2][2] && board[0][0] > 0) {
		return board[0][0];
	} else if (board[0][2] == board[1][1] && board[0][2] == board[2][0] && board[0][2] > 0) {
		return board[0][2];
	}

	//If the game hasn't been won yet, it just returns a -1
	return -1;
}



//Checks to see if the game is in a stalemate
bool CheckStalemate(int board[3][3]) {
	
	//The bool that is returned
	bool isFull = true;

	for (int x = 0; x < 3; x++) {
		for (int y = 0; y < 3; y++) {
			if (board[x][y] == 0) {
				isFull = false;
			}
		}
	}

	//Returns the value
	return isFull;
}



//Prints the board
void PrintBoard(int board[3][3]) {
	for (int y = 0; y < 3; y++) {
		for (int x = 0; x < 3; x++) {
			cout << board[x][y];
		}
		cout << endl;
	}
}



//This makes sure that the board is properly set up
void SetUpBoard(int board[3][3]) {
	for (int x = 0; x < 3; x++) {
		for (int y = 0; y < 3; y++) {
			board[x][y] = 0;
		}
	}
}



//This is the random AI
void RandAITakeTurn(int tempBoard[3][3]) {

	//Variables
	int choiceBoard[3][3];
	int choice;
	int total = 0;

	//Sets up the board for decision making
	for (int x = 0; x < 3; x++) {
		for (int y = 0; y < 3; y++) {
			if (tempBoard[x][y] == 0) {
				choiceBoard[x][y] = 1;
				total = total + 1;
			}
			else {
				choiceBoard[x][y] = 0;
			}
		}
	}

	//Just a statement
	cout << '\n' << "Deciding..." << endl;

	//Generates random numbers
	srand(time(NULL));
	choice = rand() % (total) + 1;
	cout << "Choice: " << choice << endl;
	cout << "Total: " << total << endl;

	for (int x = 0; x < 3; x++) {
		for (int y = 0; y < 3; y++) {
			if (choiceBoard[x][y] == 1) {
				choice = choice - 1;
			}
			if (choice < 1) {
				tempBoard[x][y] = 2;
				x = 5;
				y = 5;
			}
		}
	}
	cout << endl;
}

void PlayerTakeTurn(int current, int tempBoard[3][3]) {
	
	//Variables
	int x;
	int y;

	//Promts user for x and y positions
	while (true) {
		cout << '\n' << "What x position should " << current << " be?" << endl;
		cin >> x;
		cout << "What y position should " << current << " be?" << endl;
		cin >> y;
		cout << endl;
		if (tempBoard[x][y] == 0) {
			break;
		}
		else {
			cout << "Position occupied. Try again" << endl;
		}
	}

	//"Returns" the move via a pass-by-reference array
	tempBoard[x][y] = current;
}

void Game() {

	//Variables
	int result = -1;
	int current;
	int board[3][3];

	//Determine who goes first
	cout << "Who goes first? 1 or 2?" << endl;
	cin >> current;
	
	//Sets up the board
	SetUpBoard(board);

	//Runs the game from there
	while (result == -1) {

		//Has the player take their turn
		PlayerTakeTurn(current, board);

		//Prints and updates the board
		PrintBoard(board);

		//Checks to see if a player has won and, if no rematches are made, keeps the victory
		result = CheckWin(board);
		if (result > 0) {
			cout << '\n' << current << " won! Press 0 for a rematch:" << endl;
			cin >> current;
			cout << endl;
			if (current == 0) {
				Game();
			}
		}
		else {
			if (current == 1) {
				current = 2;
			}
			else {
				current = 1;
			}
		}

		//Finally, we can check for a stalemate
		if (CheckStalemate(board)) {
			result = 3;
			cout << '\n' << "Stalemate. Press 0 for a rematch:" << endl;
			cin >> current;
			cout << endl;
			if (current == 0) {
				Game();
			}
		}
	}
}

void AIGame(TTTAI player) {

}

void ComGame() {
	
	//Variables
	int result = -1;
	int current;
	int board[3][3];

	//Determine who goes first
	cout << "Who goes first? 1 or 2?" << endl;
	cin >> current;

	//Sets up the board
	SetUpBoard(board);

	//Runs the game
	while (result == -1) {
		
		//Either the player or computer determines their move
		if (current == 1) {
			PlayerTakeTurn(1, board);
		}
		else {
			RandAITakeTurn(board);
		}

		//Prints and updates the board
		PrintBoard(board);

		//Checks to see if a player has won and, if no rematches are made, keeps the victory
		result = CheckWin(board);
		if (result > 0) {
			cout << '\n' << current << " won! Press 0 for a rematch:" << endl;
			cin >> current;
			cout << endl;
			if (current == 0) {
				ComGame();
			}
		}
		else {
			if (current == 1) {
				current = 2;
			}
			else {
				current = 1;
			}
		}

		//Finally, we can check for a stalemate
		if (CheckStalemate(board)) {
			result = 3;
			cout << '\n' << "Stalemate. Press 0 for a rematch:" << endl;
			cin >> current;
			cout << endl;
			if (current == 0) {
				ComGame();
			}
		}
	}
}

void TakeTurn(int tempBoard[3][3]) {

}

//Depending on the menu variable, this will handle each menu
int MenuFunction(int n) {

	int response;

	cout << "1 - Play verses a computer" << endl;
	cout << "2 - Play verses a player" << endl;
	cout << "3 - Play against the AI(No changes will be made)" << endl;
	cout << "4 - Save the AI" << endl;
	cout << "5 - Load AI data" << endl;
	cout << "6 - Training the AI (Montage not included)" << endl;
	cout << "7 - THE SHOWDOWN" << endl;
	cout << "8 - Retrieve general TTTAI data" << endl;
	cout << "9 - Test game over text document" << endl;
	cout << "-1 - exit" << endl;
	cout << '\n' << "Decision:" << endl;
	
	cin >> response;

	return response;
}

int main() {
	
	int menu = 0;
	int response;
	bool running = true;
	TTTAI dynamicBot;
	ifstream inArena;
	ofstream outArena;

	//Manages the menu
	while (running == true) {
		response = MenuFunction(menu);
		if (response == -1) {
			running = false;
		} else if (response == 1) {
			ComGame();
		} else if (response == 2) {
			Game();
		}
	}
}
