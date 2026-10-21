# ============================================================
# Practical Number : 3
# Practical Title  : A* Search for the 8-Puzzle Problem
#
# Aim:
#   To implement the A* search algorithm to solve the 8-Puzzle using
#   the Manhattan Distance heuristic.
#
# Theory:
#   The 8-Puzzle is a 3x3 board with tiles 1-8 and one blank (0).
#   A move slides a tile into the blank, which is the same as moving
#   the blank UP, DOWN, LEFT or RIGHT. A* is an informed search that
#   always expands the node with the smallest value of
#           f(n) = g(n) + h(n)
#   where g(n) is the cost from the start (number of moves so far) and
#   h(n) is the estimated cost to the goal. We use the Manhattan Distance
#   (sum over tiles of |row difference| + |column difference|) as h(n).
#   It never overestimates the true cost (it is admissible), so A* is
#   guaranteed to find a shortest solution. Only half of all 8-Puzzle
#   states are solvable; a state is solvable when the number of
#   inversions in the tile sequence (ignoring the blank) is even.
#
# Algorithm:
#   1. If the start state is unsolvable (odd inversions), stop.
#   2. Put the start state in the OPEN list (priority queue ordered by f).
#   3. Remove the state with the lowest f from OPEN.
#   4. If it is the goal, build the path using the parent links and stop.
#   5. Add it to the CLOSED (visited) set.
#   6. Generate each valid successor by sliding the blank.
#   7. Skip successors in CLOSED. For the others compute g = g + 1,
#      h = Manhattan distance, f = g + h. If this is a cheaper way to
#      reach the successor, record its parent and push it into OPEN.
#   8. Repeat from step 3 until OPEN is empty.
#
# Expected Outcome:
#   For solvable boards the program prints every board of the solution
#   path and the total number of moves (the minimum possible).
#   For an unsolvable board it reports that no solution exists.
# ============================================================

import heapq

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)


def count_inversions(state):
    """Count pairs of tiles that are in the wrong order (blank ignored)."""
    tiles = []
    for value in state:
        if value != 0:
            tiles.append(value)
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions = inversions + 1
    return inversions


def is_solvable(state):
    # For a 3x3 puzzle (odd width) the state is solvable iff inversions are even
    return count_inversions(state) % 2 == 0


def manhattan_distance(state):
    """Heuristic h(n): sum of distances of each tile from its goal cell."""
    total = 0
    for index in range(9):
        tile = state[index]
        if tile != 0:
            goal_index = GOAL_STATE.index(tile)
            row_difference = abs(index // 3 - goal_index // 3)
            col_difference = abs(index % 3 - goal_index % 3)
            total = total + row_difference + col_difference
    return total


def get_successors(state):
    """Generate all valid states reachable by moving the blank once."""
    successors = []
    blank = state.index(0)
    row = blank // 3
    col = blank % 3

    # (move name, row change, column change)
    moves = [("UP", -1, 0), ("DOWN", 1, 0), ("LEFT", 0, -1), ("RIGHT", 0, 1)]
    for name, d_row, d_col in moves:
        new_row = row + d_row
        new_col = col + d_col
        if 0 <= new_row < 3 and 0 <= new_col < 3:      # stay on the board
            new_blank = new_row * 3 + new_col
            new_state = list(state)
            # swap blank with the neighbouring tile
            new_state[blank] = new_state[new_blank]
            new_state[new_blank] = 0
            successors.append((name, tuple(new_state)))
    return successors


def print_board(state):
    for r in range(3):
        line = ""
        for c in range(3):
            value = state[r * 3 + c]
            if value == 0:
                line = line + "_ "
            else:
                line = line + str(value) + " "
        print("    " + line)


def a_star(start_state):
    if not is_solvable(start_state):
        return None, 0

    counter = 0                      # tie-breaker so the heap never compares states
    start_h = manhattan_distance(start_state)
    open_list = [(start_h, counter, 0, start_state)]   # (f, counter, g, state)

    best_g = {start_state: 0}        # cheapest known cost to reach each state
    parent = {start_state: None}     # state -> (previous state, move)
    closed = set()                   # visited (already expanded) states
    expanded = 0

    while len(open_list) > 0:
        f, _, g, current = heapq.heappop(open_list)

        if current in closed:        # stale queue entry, ignore
            continue

        if current == GOAL_STATE:
            # Rebuild the path from goal back to start
            path = []
            moves = []
            node = current
            while node is not None:
                path.append(node)
                if parent[node] is not None:
                    moves.append(parent[node][1])
                    node = parent[node][0]
                else:
                    node = None
            path.reverse()
            moves.reverse()
            return (path, moves), expanded

        closed.add(current)
        expanded = expanded + 1

        for move_name, next_state in get_successors(current):
            if next_state in closed:
                continue
            new_g = g + 1
            if next_state not in best_g or new_g < best_g[next_state]:
                best_g[next_state] = new_g
                parent[next_state] = (current, move_name)
                new_f = new_g + manhattan_distance(next_state)
                counter = counter + 1
                heapq.heappush(open_list, (new_f, counter, new_g, next_state))

    return None, expanded


def solve_and_display(title, start_state):
    print(title)
    print("Start state:")
    print_board(start_state)
    print("Goal state:")
    print_board(GOAL_STATE)
    print("Inversions = " + str(count_inversions(start_state)) +
          ", initial Manhattan distance = " + str(manhattan_distance(start_state)))

    result, expanded = a_star(start_state)

    if result is None:
        print("RESULT: This puzzle is UNSOLVABLE (odd number of inversions).")
    else:
        path = result[0]
        moves = result[1]
        print("Solution found! States expanded: " + str(expanded))
        for i in range(len(path)):
            if i == 0:
                print("  Initial state:")
            else:
                print("  Move " + str(i) + ": blank moves " + moves[i - 1])
            print_board(path[i])
        print("Total moves = " + str(len(moves)))
        print("Move sequence: " + (", ".join(moves) if len(moves) > 0 else "(none)"))
    print("=" * 60)


# ---------- Main program ----------
if __name__ == "__main__":
    print("A* SEARCH FOR THE 8-PUZZLE (Manhattan Distance heuristic)")
    print("Blank tile is shown as _")
    print("=" * 60)

    # Test 1: easy puzzle
    solve_and_display("TEST 1: Easy puzzle", (1, 2, 3,
                                              4, 0, 6,
                                              7, 5, 8))

    # Test 2: medium puzzle
    solve_and_display("TEST 2: Medium puzzle", (1, 2, 3,
                                                5, 0, 6,
                                                4, 7, 8))

    # Test 3: harder puzzle
    solve_and_display("TEST 3: Harder puzzle", (8, 1, 3,
                                                4, 0, 2,
                                                7, 6, 5))

    # Test 4: already solved (edge case)
    solve_and_display("TEST 4: Already solved", GOAL_STATE)

    # Test 5: unsolvable puzzle (edge case; tiles 7 and 8 swapped)
    solve_and_display("TEST 5: Unsolvable puzzle", (1, 2, 3,
                                                    4, 5, 6,
                                                    8, 7, 0))
