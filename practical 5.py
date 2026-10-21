# ============================================================
# Practical Number : 5
# Practical Title  : Blocks World Planning using Breadth First Search
#
# Aim:
#   To solve the Blocks World planning problem using Breadth First
#   Search (BFS) and to display the sequence of actions that leads from
#   the initial configuration to the goal configuration.
#
# Theory:
#   Planning means finding a sequence of actions that transforms an
#   initial state into a goal state. In the Blocks World, blocks lie on
#   a table (which has room for any number of blocks) or on top of each
#   other. Only a block with nothing on top of it ("clear") can be moved,
#   and only one block moves at a time. A block can be moved onto the
#   table or onto another clear block. Each arrangement of blocks is a
#   STATE and each legal move is an ACTION. BFS explores states level
#   by level using a queue, so the first plan it finds to the goal is the
#   SHORTEST plan (fewest actions). A visited collection prevents the
#   same state from being explored twice.
#
# Algorithm:
#   1. A state is a collection of stacks; each stack lists blocks from
#      bottom to top. Stacks are kept sorted so equal states look equal.
#   2. Put the initial state in a queue and mark it visited.
#   3. Remove the first state from the queue.
#   4. If it equals the goal state, rebuild the plan from parent links.
#   5. Generate legal successors: take the top block of any stack and
#      move it (a) onto the top of another stack or (b) to the table
#      (if it is not already alone on the table).
#   6. For each successor not yet visited: mark it visited, store its
#      parent and the action used, and add it to the queue.
#   7. If the queue becomes empty, no plan exists.
#
# Expected Outcome:
#   The program prints the initial and goal configurations, the list of
#   actions in order with the state after each action, and the number
#   of actions in the shortest plan.
# ============================================================

from collections import deque


def make_state(list_of_stacks):
    """Canonical form: tuple of tuples, sorted, so order of stacks is irrelevant."""
    stacks = []
    for stack in list_of_stacks:
        if len(stack) > 0:
            stacks.append(tuple(stack))
    stacks.sort()
    return tuple(stacks)


def get_successors(state):
    """Return list of (action_text, new_state) for every legal move."""
    successors = []
    for i in range(len(state)):
        block = state[i][-1]                  # only the top (clear) block can move

        # (a) Move the block onto the top of another stack
        for j in range(len(state)):
            if i == j:
                continue
            new_stacks = [list(s) for s in state]
            new_stacks[i].pop()
            new_stacks[j].append(block)
            if len(state[i]) > 1:
                action = "Move " + block + " from top of " + state[i][-2] + " onto " + state[j][-1]
            else:
                action = "Move " + block + " from table onto " + state[j][-1]
            successors.append((action, make_state(new_stacks)))

        # (b) Move the block to the table (useless if it is already alone)
        if len(state[i]) > 1:
            new_stacks = [list(s) for s in state]
            new_stacks[i].pop()
            new_stacks.append([block])
            action = "Move " + block + " from top of " + state[i][-2] + " to table"
            successors.append((action, make_state(new_stacks)))
    return successors


def show_state(state):
    """Draw the blocks; the table is the line at the bottom."""
    tallest = 0
    for stack in state:
        if len(stack) > tallest:
            tallest = len(stack)
    for level in range(tallest - 1, -1, -1):
        line = "      "
        for stack in state:
            if level < len(stack):
                line = line + "[" + stack[level] + "] "
            else:
                line = line + "    "
        print(line)
    print("      " + "----" * len(state) + "  (table)")


def bfs_plan(initial_state, goal_state):
    queue = deque([initial_state])
    visited = set([initial_state])
    parent = {initial_state: None}       # state -> (previous state, action)

    while len(queue) > 0:
        current = queue.popleft()

        if current == goal_state:
            plan = []
            node = current
            while parent[node] is not None:
                previous, action = parent[node]
                plan.append((action, node))
                node = previous
            plan.reverse()
            return plan, len(visited)

        for action, new_state in get_successors(current):
            if new_state not in visited:
                visited.add(new_state)
                parent[new_state] = (current, action)
                queue.append(new_state)

    return None, len(visited)


def solve(title, initial_state, goal_state):
    print(title)
    print("Initial configuration:")
    show_state(initial_state)
    print("Goal configuration:")
    show_state(goal_state)

    plan, visited_count = bfs_plan(initial_state, goal_state)
    if plan is None:
        print("No plan exists.")
    elif len(plan) == 0:
        print("Initial state already equals the goal. Plan has 0 actions.")
    else:
        print("Plan found (states visited by BFS: " + str(visited_count) + ")")
        step = 1
        for action, state in plan:
            print("  Step " + str(step) + ": " + action)
            show_state(state)
            step = step + 1
        print("Total actions in plan = " + str(len(plan)))
    print("=" * 60)


# ---------- Main program ----------
if __name__ == "__main__":
    print("BLOCKS WORLD PLANNING USING BFS")
    print("Each stack is written bottom -> top in the code; drawn upright here.")
    print("=" * 60)

    # Test 1: A sits on C, B is alone. Goal: tower A on B on C.
    start_1 = make_state([["C", "A"], ["B"]])
    goal_1 = make_state([["C", "B", "A"]])
    solve("TEST 1: 3 blocks", start_1, goal_1)

    # Test 2: reverse a tower of 4 blocks
    start_2 = make_state([["A", "B", "C", "D"]])
    goal_2 = make_state([["D", "C", "B", "A"]])
    solve("TEST 2: 4 blocks, reverse the tower", start_2, goal_2)

    # Test 3: already at goal (edge case)
    start_3 = make_state([["A", "B"], ["C"]])
    solve("TEST 3: Initial state equals goal", start_3, start_3)
