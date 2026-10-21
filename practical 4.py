# ============================================================
# Practical Number : 4
# Practical Title  : Tower of Hanoi using State Space Search
#
# Aim:
#   To solve the Tower of Hanoi puzzle by searching its state space
#   (Breadth First Search) and to display every transition.
#
# Theory:
#   In Tower of Hanoi there are three rods (A, B, C) and N disks of
#   different sizes stacked on rod A with the largest at the bottom.
#   Rules: move only one disk at a time, only the TOP disk of a rod can
#   be moved, and a larger disk may never be placed on a smaller one.
#   In state space search, every arrangement of the disks is a STATE,
#   a legal move is a TRANSITION, the initial state has all disks on A,
#   and the goal state has all disks on C. Breadth First Search explores
#   the states level by level, so the first time it reaches the goal it
#   has found a solution with the minimum number of moves, which is
#   2^N - 1 for N disks.
#
# Algorithm:
#   1. Represent a state as three lists (rods A, B, C); disks are
#      numbers (1 = smallest) listed from bottom to top.
#   2. Put the initial state in a queue and mark it visited.
#   3. Remove the first state from the queue.
#   4. If it is the goal state (all disks on rod C), stop.
#   5. For every pair of rods (from, to): if "from" is not empty and its
#      top disk is smaller than the top disk of "to" (or "to" is empty),
#      create the new state, and if it is not visited, store its parent
#      and add it to the queue.
#   6. Repeat from step 3.
#   7. Follow the parent links back from the goal to print the solution.
#
# Expected Outcome:
#   For 3 disks the program prints all 7 moves with the state of the rods
#   after each move, then the total number of moves and the goal state.
#   A summary for 1 to 4 disks confirms the minimum moves are 2^N - 1.
# ============================================================

from collections import deque

RODS = ["A", "B", "C"]


def make_initial_state(number_of_disks):
    # All disks on rod A, largest (N) at the bottom, smallest (1) on top
    rod_a = []
    for disk in range(number_of_disks, 0, -1):
        rod_a.append(disk)
    return (tuple(rod_a), (), ())


def is_goal(state, number_of_disks):
    return len(state[2]) == number_of_disks


def get_successors(state):
    """Return a list of (disk, from_rod, to_rod, new_state) for legal moves."""
    successors = []
    for source in range(3):
        for target in range(3):
            if source == target:
                continue
            if len(state[source]) == 0:
                continue                                  # nothing to move
            disk = state[source][-1]                      # top disk
            if len(state[target]) > 0 and state[target][-1] < disk:
                continue                                  # larger on smaller: illegal

            # Build the new state
            new_rods = [list(state[0]), list(state[1]), list(state[2])]
            new_rods[source].pop()
            new_rods[target].append(disk)
            new_state = (tuple(new_rods[0]), tuple(new_rods[1]), tuple(new_rods[2]))
            successors.append((disk, RODS[source], RODS[target], new_state))
    return successors


def show_state(state):
    for i in range(3):
        print("      Rod " + RODS[i] + ": " + str(list(state[i])))


def solve_hanoi(number_of_disks):
    """BFS over the state space. Returns the list of (disk, from, to, state)."""
    start = make_initial_state(number_of_disks)
    queue = deque([start])
    visited = set([start])
    parent = {start: None}          # state -> (previous state, disk, from, to)
    states_explored = 0

    while len(queue) > 0:
        current = queue.popleft()
        states_explored = states_explored + 1

        if is_goal(current, number_of_disks):
            # Walk back through parents to collect the moves
            steps = []
            node = current
            while parent[node] is not None:
                previous, disk, from_rod, to_rod = parent[node]
                steps.append((disk, from_rod, to_rod, node))
                node = previous
            steps.reverse()
            return start, steps, states_explored

        for disk, from_rod, to_rod, new_state in get_successors(current):
            if new_state not in visited:
                visited.add(new_state)
                parent[new_state] = (current, disk, from_rod, to_rod)
                queue.append(new_state)

    return start, [], states_explored


# ---------- Main program ----------
if __name__ == "__main__":
    print("TOWER OF HANOI USING STATE SPACE SEARCH (BFS)")
    print("=" * 60)

    disks = 3
    start_state, solution, explored = solve_hanoi(disks)

    print("Number of disks : " + str(disks))
    print("Total states in the space: 3^" + str(disks) + " = " + str(3 ** disks))
    print("Initial state (disks listed bottom -> top):")
    show_state(start_state)
    print("-" * 60)

    move_number = 1
    for disk, from_rod, to_rod, state in solution:
        print("Move " + str(move_number) + ": Move disk " + str(disk) +
              " from rod " + from_rod + " to rod " + to_rod)
        show_state(state)
        move_number = move_number + 1

    print("-" * 60)
    print("Total number of moves = " + str(len(solution)))
    print("Minimum possible (2^N - 1) = " + str(2 ** disks - 1))
    print("States explored by BFS = " + str(explored))
    print("GOAL STATE reached (all disks on rod C):")
    show_state(solution[-1][3])
    print("=" * 60)

    # Verify the minimum-move formula for other sizes
    print("Summary for different numbers of disks:")
    print("Disks | BFS moves | 2^N - 1")
    for n in range(1, 5):
        a, steps, e = solve_hanoi(n)
        print("  " + str(n) + "   |    " + str(len(steps)).ljust(7) + "  |   " + str(2 ** n - 1))
