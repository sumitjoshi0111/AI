# ============================================================
# Practical Number : 6
# Practical Title  : 8-Queens Problem using Backtracking Search (CSP)
#
# Aim:
#   To solve the 8-Queens Constraint Satisfaction Problem using the
#   Backtracking search algorithm.
#
# Theory:
#   The 8-Queens problem asks us to place 8 queens on an 8x8 chessboard
#   so that no two queens attack each other. As a Constraint Satisfaction
#   Problem (CSP): the VARIABLES are the 8 rows (one queen per row), the
#   DOMAIN of each variable is the column number 0-7, and the CONSTRAINTS
#   are that no two queens share a column or a diagonal (rows are already
#   different). Backtracking is a depth-first search that assigns values
#   to variables one by one. After each assignment it checks the
#   constraints; if a constraint is violated the value is rejected, and
#   if no value works for a variable the algorithm goes back to the
#   previous variable and tries its next value. This prunes large parts
#   of the search space compared with trying all placements.
#
# Algorithm:
#   1. Start with row 0 and an empty board.
#   2. If all 8 rows have a queen, a solution is found.
#   3. For each column 0..7 in the current row:
#        a. Check that no earlier queen is in the same column.
#        b. Check that no earlier queen is on the same diagonal
#           (|row difference| == |column difference|).
#        c. If safe, place the queen and recursively solve the next row.
#        d. If the recursive call fails, remove the queen (backtrack)
#           and try the next column.
#   4. If no column works in this row, return failure to the caller.
#
# Expected Outcome:
#   A valid 8x8 board with 8 non-attacking queens is printed together
#   with the queen positions. The program also counts all solutions
#   (92 for 8 queens) to confirm that the algorithm is correct.
# ============================================================

BOARD_SIZE = 8


def is_safe(queen_columns, row, col):
    """Check row/column/diagonal constraints against queens in rows above."""
    for previous_row in range(row):
        previous_col = queen_columns[previous_row]

        # Column constraint
        if previous_col == col:
            return False

        # Diagonal constraint
        if abs(previous_col - col) == abs(previous_row - row):
            return False
    # (Row constraint is automatic: we place only one queen per row.)
    return True


def solve_queens(queen_columns, row, counters):
    """Place queens row by row. Returns True when all rows are filled."""
    if row == BOARD_SIZE:
        return True

    for col in range(BOARD_SIZE):
        counters["tries"] = counters["tries"] + 1
        if is_safe(queen_columns, row, col):
            queen_columns[row] = col                 # place queen
            if solve_queens(queen_columns, row + 1, counters):
                return True
            queen_columns[row] = -1                  # backtrack: remove queen
            counters["backtracks"] = counters["backtracks"] + 1
    return False


def count_all_solutions(queen_columns, row):
    """Same backtracking, but keeps going to count every solution."""
    if row == BOARD_SIZE:
        return 1
    total = 0
    for col in range(BOARD_SIZE):
        if is_safe(queen_columns, row, col):
            queen_columns[row] = col
            total = total + count_all_solutions(queen_columns, row + 1)
            queen_columns[row] = -1
    return total


def print_board(queen_columns):
    print("      " + " ".join([str(c) for c in range(BOARD_SIZE)]))
    print("      " + "-" * (2 * BOARD_SIZE - 1))
    for row in range(BOARD_SIZE):
        line = ""
        for col in range(BOARD_SIZE):
            if queen_columns[row] == col:
                line = line + "Q "
            else:
                line = line + ". "
        print("  " + str(row) + " | " + line)


def verify_solution(queen_columns):
    """Independent check: compare every pair of queens."""
    for r1 in range(BOARD_SIZE):
        for r2 in range(r1 + 1, BOARD_SIZE):
            c1 = queen_columns[r1]
            c2 = queen_columns[r2]
            if c1 == c2 or abs(c1 - c2) == abs(r1 - r2):
                return False
    return True


# ---------- Main program ----------
if __name__ == "__main__":
    print("8-QUEENS PROBLEM USING BACKTRACKING")
    print("=" * 60)

    queen_columns = [-1] * BOARD_SIZE         # queen_columns[row] = column of queen
    counters = {"tries": 0, "backtracks": 0}

    found = solve_queens(queen_columns, 0, counters)

    if found:
        print("A valid solution was found.")
        print("Queen positions (row, column):")
        for row in range(BOARD_SIZE):
            print("  Queen " + str(row + 1) + ": (" + str(row) + ", " + str(queen_columns[row]) + ")")
        print()
        print("Final 8x8 chessboard (Q = queen):")
        print_board(queen_columns)
        print()
        print("Column positions by row: " + str(queen_columns))
        print("Positions tried: " + str(counters["tries"]) +
              ", backtracks: " + str(counters["backtracks"]))
        print("Independent verification (no two queens attack): " +
              str(verify_solution(queen_columns)))
    else:
        print("No solution found.")

    print("=" * 60)
    total = count_all_solutions([-1] * BOARD_SIZE, 0)
    print("Total number of distinct solutions for 8 queens = " + str(total))
    print("(Known correct value is 92)")
