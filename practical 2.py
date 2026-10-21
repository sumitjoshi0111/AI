# ============================================================
# Practical Number : 2
# Practical Title  : Model-Based Agent Navigating a Grid with Obstacles
#
# Aim:
#   To implement a model-based intelligent agent that navigates a 2D
#   grid containing obstacles from a start cell to a goal cell using
#   an internal state representation.
#
# Theory:
#   A model-based agent keeps INTERNAL STATE: a model of the world that
#   is updated from every percept. This lets it work in a partially
#   observable environment. Here the agent cannot see the whole grid.
#   At each cell it only senses its four neighbours (UP, DOWN, LEFT,
#   RIGHT) and learns whether each is FREE or a WALL. The agent stores
#   what it has learned in a map (known cells), a set of visited cells
#   and a stack holding the path it has followed. Because visited cells
#   are remembered, the agent never walks into a loop. When it reaches a
#   dead end it BACKTRACKS along its stack. This is depth-first
#   exploration guided by a Manhattan-distance preference toward the goal.
#
# Algorithm:
#   1. Start at the start cell; push it on the path stack; mark visited.
#   2. Sense the four neighbours and update the internal map.
#   3. If the current cell is the goal, stop: the stack is the path.
#   4. Collect neighbours that are FREE and not yet visited.
#   5. If there are some, move to the one closest (Manhattan distance)
#      to the goal; mark it visited and push it on the stack.
#   6. If there are none (dead end), pop the stack and move back to the
#      previous cell (backtrack).
#   7. If the stack becomes empty, the goal is unreachable; stop.
#   8. Repeat from step 2.
#
# Expected Outcome:
#   The agent reaches the goal while avoiding obstacles and never
#   repeating a state in a loop. The final path and the grid with the
#   path marked are displayed. A second test shows an unreachable goal.
# ============================================================

# Direction name -> (row change, column change)
DIRECTIONS = [("UP", -1, 0), ("DOWN", 1, 0), ("LEFT", 0, -1), ("RIGHT", 0, 1)]


def sense_neighbours(real_grid, position):
    """Percept: what is in the four neighbouring cells (FREE or WALL)."""
    row = position[0]
    col = position[1]
    percept = {}
    for name, d_row, d_col in DIRECTIONS:
        new_row = row + d_row
        new_col = col + d_col
        inside = 0 <= new_row < len(real_grid) and 0 <= new_col < len(real_grid[0])
        if inside and real_grid[new_row][new_col] != "#":
            percept[(new_row, new_col)] = "FREE"
        else:
            percept[(new_row, new_col)] = "WALL"
    return percept


def manhattan(cell_1, cell_2):
    return abs(cell_1[0] - cell_2[0]) + abs(cell_1[1] - cell_2[1])


def print_grid(real_grid, path, agent_position):
    """Draw the grid. '*' = path, 'A' = agent, '#' = wall, S/G as given."""
    for r in range(len(real_grid)):
        line = ""
        for c in range(len(real_grid[0])):
            cell = real_grid[r][c]
            if (r, c) == agent_position:
                line = line + "A "
            elif (r, c) in path and cell == ".":
                line = line + "* "
            else:
                line = line + cell + " "
        print("   " + line)


def find_cell(real_grid, symbol):
    for r in range(len(real_grid)):
        for c in range(len(real_grid[0])):
            if real_grid[r][c] == symbol:
                return (r, c)
    return None


def run_agent(real_grid):
    start = find_cell(real_grid, "S")
    goal = find_cell(real_grid, "G")

    # ----- Internal state of the agent -----
    known_map = {}              # cell -> "FREE" or "WALL"
    visited = set()             # cells already entered
    path_stack = [start]        # current path from start to agent
    visited.add(start)
    known_map[start] = "FREE"

    position = start
    step = 0
    max_steps = 1000            # safety limit (cannot be reached normally)

    print("Start = " + str(start) + ", Goal = " + str(goal))
    print("Agent senses only its 4 neighbours at each step.")
    print("-" * 60)

    while step < max_steps:
        # 1. Sense and update internal model
        percept = sense_neighbours(real_grid, position)
        for cell in percept:
            known_map[cell] = percept[cell]

        # 2. Goal test
        if position == goal:
            print("Step " + str(step) + ": at " + str(position) + " -> GOAL REACHED")
            break

        # 3. Choose among FREE, unvisited neighbours (the model prevents loops)
        candidates = []
        for cell in percept:
            if known_map[cell] == "FREE" and cell not in visited:
                candidates.append(cell)

        step = step + 1
        if len(candidates) > 0:
            # Pick the candidate closest to the goal
            best = candidates[0]
            for cell in candidates:
                if manhattan(cell, goal) < manhattan(best, goal):
                    best = cell
            print("Step " + str(step) + ": " + str(position) + " -> MOVE to " + str(best) +
                  "   (known cells: " + str(len(known_map)) +
                  ", visited: " + str(len(visited) + 1) + ")")
            position = best
            visited.add(position)
            path_stack.append(position)
        else:
            # Dead end: backtrack
            path_stack.pop()
            if len(path_stack) == 0:
                print("Step " + str(step) + ": no moves left and nothing to backtrack to.")
                print("RESULT: Goal is UNREACHABLE.")
                return None
            previous = path_stack[len(path_stack) - 1]
            print("Step " + str(step) + ": " + str(position) + " -> DEAD END, BACKTRACK to " +
                  str(previous))
            position = previous

    print("-" * 60)
    print("Final path (" + str(len(path_stack) - 1) + " moves):")
    print("  " + " -> ".join([str(cell) for cell in path_stack]))
    print("Grid with final path (A = agent, * = path):")
    print_grid(real_grid, path_stack, position)
    return path_stack


# ---------- Main program ----------
if __name__ == "__main__":
    print("MODEL-BASED AGENT: GRID NAVIGATION")
    print("Legend: S = start, G = goal, # = obstacle, . = free cell")
    print("=" * 60)

    # TEST 1: a grid where a path exists and the agent meets a dead end
    grid_1 = [
        list("S...#."),
        list(".##.#."),
        list("....#."),
        list(".####."),
        list("......"),
        list("#.#.#G"),
    ]
    print("TEST 1: Reachable goal")
    print("Real environment (hidden from the agent):")
    print_grid(grid_1, [], None)
    run_agent(grid_1)

    print()
    print("=" * 60)

    # TEST 2: goal is completely walled off
    grid_2 = [
        list("S..."),
        list(".##."),
        list(".#G#"),
        list("..##"),
    ]
    print("TEST 2: Unreachable goal (edge case)")
    print("Real environment (hidden from the agent):")
    print_grid(grid_2, [], None)
    run_agent(grid_2)
