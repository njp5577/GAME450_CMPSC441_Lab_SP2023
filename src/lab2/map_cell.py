'''
Extra Credit Task-

Tic tac toe input
Here's the backstory for this challenge: imagine you're writing a tic-tac-toe game, where the board looks like this:

1:  X | O | X
   -----------
2:    |   |  
   -----------
3:  O |   |
    A   B   C
The board is represented as a 2D list:

board = [
    ["X", "O", "X"],
    [" ", " ", " "],
    ["O", " ", " "],
]
Imagine if your user enters "C1" and you need to see if there's an X or O in that cell on the board. To do so, you need to translate from the string "C1" to row 0 and column 2 so that you can check board[row][column].

Your task is to write a function that can translate from strings of length 2 to a tuple (row, column). Name your function get_row_col; it should take a single parameter which is a string of length 2 consisting of an uppercase letter and a digit.

For example, calling get_row_col("A3") should return the tuple (2, 0) because A3 corresponds to the row at index 2 and column at index 0in the board.
'''
#Function for converting entered cell on board to a tuple with the location in integers
def get_row_col(board_string):
    #Start with an empty tuple
    board_loc = ()

    #Since the values need to be swapped to produce the correct output, we will start by converting the number at the end
    for number in ('1', '2', '3'):
        if number == board_string[1]:
            if number == '1':
                board_loc = board_loc + (0,)
            elif number == '2':
                board_loc = board_loc + (1,)
            elif number == '3':
                board_loc = board_loc + (2,)
    
    #Then convert the character at the start to an integer
    for letter in ('A', 'B', 'C'):
        if letter == board_string[0]:
            if letter == 'A':
                board_loc = board_loc + (0,)
            elif letter == 'B':
                board_loc = board_loc + (1,)
            elif letter == 'C':
                board_loc = board_loc + (2,)

    #Return the converted cell location
    return board_loc

#Main to test the function
if __name__ == '__main__':
    print(get_row_col("A1"))
    print(get_row_col("A2"))
    print(get_row_col("A3"))
    print(get_row_col("B1"))
    print(get_row_col("B2"))
    print(get_row_col("B3"))
    print(get_row_col("C1"))
    print(get_row_col("C2"))
    print(get_row_col("C3"))