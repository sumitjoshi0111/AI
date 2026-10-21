# ============================================================
# Practical Number : 8
# Practical Title  : Tic-Tac-Toe using the Minimax Algorithm
#
# Aim:
#   To develop a game-playing agent that uses the Minimax algorithm to
#   make optimal decisions in Tic-Tac-Toe (Human vs Computer).
#
# Theory:
#   Tic-Tac-Toe is a two-player, zero-sum, perfect-information game.
#   Minimax searches the complete game tree. The two players are MAX
#   (the computer, who tries to maximize the score) and MIN (the human,
#   who is assumed to play perfectly and tries to minimize the score).
#   A TERMINAL state is one where someone has won or the board is full.
#   Its utility is: computer wins = +10, human wins = -10, draw = 0.
#   We subtract the depth from a win (and add it to a loss) so that the
#   computer prefers quick wins and delays defeat. Scores from the
#   terminal states are passed back up the tree: MAX nodes take the
#   largest child value and MIN nodes take the smallest. The computer
#   plays the move with the highest minimax value, so it never loses.
#
# Algorithm:
#   minimax(board, whose_turn, depth):
#   1. If the computer has won, return 10 - depth.
#   2. If the human has won, return depth - 10.
#   3. If the board is full (draw), return 0.
#   4. If it is the computer's turn (MAX): try every empty cell, call
#      minimax for the human's turn, undo the move, and keep the
#      largest score.
#   5. If it is the human's turn (MIN): do the same but keep the
#      smallest score.
#   Computer's move: evaluate every empty cell with minimax and play
#   the cell with the highest score.
#
# Expected Outcome:
#   A playable console game. The human plays X, the computer plays O.
#   The computer plays optimally, so the result is either a computer
#   win or a draw; the human can never win. The game announces the
#   result (win, loss or draw).
# ============================================================

HUMAN = "X"
COMPUTER = "O"
EMPTY = " "

# All 8 winning lines (board positions 0..8)
WIN_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],      # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],      # columns
    [0, 4, 8], [2, 4, 6],                 # diagonals
]


def print_board(board):
    """Show the board; empty cells show their number (1-9) as a guide."""
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            index = row * 3 + col
            if board[index] == EMPTY:
                cells.append(str(index + 1))
            else:
                cells.append(board[index])
        print("   " + cells[0] + " | " + cells[1] + " | " + cells[2])
        if row < 2:
            print("  ---+---+---")
    print()


def check_winner(board):
    """Return 'X' or 'O' if that player has three in a line, else None."""
    for line in WIN_LINES:
        a = board[line[0]]
        b = board[line[1]]
        c = board[line[2]]
        if a != EMPTY and a == b and b == c:
            return a
    return None


def is_board_full(board):
    return EMPTY not in board


def is_terminal(board):
    """Terminal-state check: someone won or the board is full."""
    return check_winner(board) is not None or is_board_full(board)


def minimax(board, computer_turn, depth):
    winner = check_winner(board)
    if winner == COMPUTER:
        return 10 - depth            # computer wins (sooner is better)
    if winner == HUMAN:
        return depth - 10            # human wins (later is better for computer)
    if is_board_full(board):
        return 0                     # draw

    if computer_turn:                # MAX player
        best_score = -100
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = COMPUTER                              # try the move
                score = minimax(board, False, depth + 1)
                board[i] = EMPTY                                 # undo the move
                if score > best_score:
                    best_score = score
        return best_score
    else:                            # MIN player
        best_score = 100
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, True, depth + 1)
                board[i] = EMPTY
                if score < best_score:
                    best_score = score
        return best_score


def best_computer_move(board):
    """Choose the empty cell with the highest minimax value."""
    best_score = -100
    best_move = -1
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = COMPUTER
            score = minimax(board, False, 1)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def get_human_move(board):
    """Ask until the human enters a valid empty cell number (1-9)."""
    while True:
        text = input("Your move (1-9): ").strip()
        if not text.isdigit():
            print("Please enter a number from 1 to 9.")
            continue
        position = int(text) - 1
        if position < 0 or position > 8:
            print("Number must be between 1 and 9.")
        elif board[position] != EMPTY:
            print("That cell is already taken. Choose another.")
        else:
            return position


def play_game():
    board = [EMPTY] * 9

    print("You are X, the computer is O.")
    print("Enter the number of the cell where you want to play.")
    answer = input("Do you want to play first? (y/n): ").strip().lower()
    human_turn = (answer != "n")

    print_board(board)

    while not is_terminal(board):
        if human_turn:
            move = get_human_move(board)
            board[move] = HUMAN
        else:
            print("Computer is thinking...")
            move = best_computer_move(board)
            board[move] = COMPUTER
            print("Computer plays at cell " + str(move + 1))
        print_board(board)
        human_turn = not human_turn

    # Terminal state reached: report the result
    winner = check_winner(board)
    if winner == HUMAN:
        print("RESULT: You win!")
    elif winner == COMPUTER:
        print("RESULT: Computer wins!")
    else:
        print("RESULT: It is a draw.")


# ---------- Main program ----------
if __name__ == "__main__":
    print("TIC-TAC-TOE USING MINIMAX (Human vs Computer)")
    print("=" * 60)
    try:
        keep_playing = True
        while keep_playing:
            play_game()
            again = input("Play again? (y/n): ").strip().lower()
            keep_playing = (again == "y")
        print("Thanks for playing!")
    except EOFError:
        print()
        print("Input ended. Exiting the game.")
