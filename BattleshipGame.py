
def init_board():
	# make a blank board
	board = []
	# 10 rows, 10 columns
	for row in range(10):
		board.append([]);
		for column in range(10):
			board[row].append('w') # w for water
	return board;


def setup_player_board(board):
	# do a tuple or dictionary for name to match
	boats = [(2,"a destroyer"),(3,"a cruiser"),(3,"a submarine"),(4,"a battleship"),(5,"a carrier")]

	print("")

	row = -1;
	column = -1;
	orientation = -1;

	# check about conflicting / overlapping boats

	for boat in boats:
		row = -1;
		column = -1;
		orientation = -1;

		print_str = "For " + boat[1] + " of length " + str(boat[0]) + ": \n"
		print(print_str)
		while(orientation < 0 or orientation > 1):
			orientation = input("For boat orientation, down (0) or right (1): ")
		while(row < 0 or row > 9):
			row = input("Provide starting row (0 - 9, 0 being top): ")
			if orientation == 0:
				if (row + boat[0]) > 9: 
					print("Not a valid row start, given orientation!")
					row = -1;
		while(column < 0 or column > 9):
			column = input("Provide starting column (0 - 9, 0 being leftmost): ")
			if orientation == 1:
				if (column + boat[0]) > 9: 
					print("Not a valid column start, given orientation!")
					column = -1;

		if orientation == 0:
			for i in range(boat[0]):
                if(board[row + i][column] == 'b')
                    print("There is already a boat occupying some of these spots, please choose another place")
                    # find some way to jump back to start...
		elif orientation == 1:
			for i in range(boat[0]):
                if(board[row][column + i] == 'b')
                    print("There is already a boat occupying some of these spots, please choose another place")
                    # find some way to jump back to start...

        if orientation == 0:
            for i in range(boat[0]):
                board[row + i][column] = 'b' # b for boat
        elif orientation == 1:
            for i in range(boat[0]):
                board[row][column  + i] = 'b' # b for boat
		


def print_board(board):
	for row in board:
		print " ".join(row)

enemy = init_board()
mine = init_board()

print_board(enemy)

setup_player_board(mine)
print_board(mine)
