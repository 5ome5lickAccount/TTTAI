#pragma once
#include <iostream>
#include <string>
using namespace std;

const int WIDTH = 3;
const int HEIGHT = 3;
const int INIT_POSSIBILITIES = 10;
const int DECISION_SIZE = 1296;

class decision
{
private:
	bool settled = false;
	int board[WIDTH][HEIGHT];
	int possibilities[WIDTH][HEIGHT];
	int sum = 0;
public:

	//The default constructor
	void SetMap(int currBoard[WIDTH][HEIGHT]) {

		//This just sets up the board as well as the possibilities
		for (int x = 0; x < WIDTH; x++) {
			for (int y = 0; y < HEIGHT; y++) {
				board[x][y] = currBoard[x][y];
				if (board[x][y] > 0) {
					possibilities[x][y] = INIT_POSSIBILITIES;
					sum = sum + INIT_POSSIBILITIES;
				}
				else {
					possibilities[x][y] = 0;
				}
			}
		}
	}

	//This is just for possibilities
	void returnPossibilities(int tempBoard[3][3]) {
		for (int x = 0; x < WIDTH; x++) {
			for (int y = 0; y < HEIGHT; y++) {
				tempBoard[x][y] = possibilities[x][y];
			}
		}
	}

	//This is for returning the current board
	void returnBoard(int tempBoard[3][3]) {
		for (int x = 0; x < WIDTH; x++) {
			for (int y = 0; y < HEIGHT; y++) {
				tempBoard[x][y] = board[x][y];
			}
		}
	}
};

class TTTAI
{
private:
	int size;
	int tempBoard[WIDTH][HEIGHT];
	int board[WIDTH][HEIGHT];
	decision decisions[DECISION_SIZE];
public:

	//Default constructor
	TTTAI() {

		//Sets up the board
		size = 1;
		for (int x = 0; x < WIDTH; x++) {
			for (int y = 0; y < HEIGHT; y++) {
				tempBoard[x][y] = 0;
				board[x][y] = 0;
			}
		}

		//Sets up the first map
		decisions[0].SetMap(board);
	}

	//Prints "DATA"
	void PrintData() const {
		
		//Prints the current board
		cout << "Current Board:" << endl;
		for (int x = 0; x < WIDTH; x++) {
			for (int y = 0; y < HEIGHT; y++) {
				cout << board[x][y] << " ";
			}
			cout << endl;
		}

		cout << "Scenarios created: " << size << endl;
	}

	//This gets what the TTTAI object board is
	void getBoard(int tempBoard[WIDTH][HEIGHT]) {
		tempBoard = board;
	}

	//This writes data to a document
	//NOTE: MAKE SURE THE FILE HAS BEEN OPENED BEFORE USING WRITEDATA.
	//THIS WILL ALSO CLOSE THE FILE
	void writeData(ofstream outFile) {
		
		//This just has the placeholder board
		int tempBoard[3][3];

		//Writes the data to the file
		outFile << size << endl;
		for (int i = 0; i < size; i++) {
			
		}
	}
};
