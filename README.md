# Artificial Intelligence Laboratory

Python implementations of the eight practical assignments for the Artificial Intelligence laboratory course (Third Year Computer Engineering, SPPU). Every program is a single, independent, beginner-friendly Python file that begins with its aim, theory, algorithm and expected outcome, followed by a commented implementation and demonstrative console output.

## List of Practicals

| No. | File | Title |
|---|---|---|
| 1 | `practical 1.py` | Simple Reflex Agent for the Vacuum Cleaner World |
| 2 | `practical 2.py` | Model-Based Agent Navigating a Grid with Obstacles |
| 3 | `practical 3.py` | A* Search for the 8-Puzzle |
| 4 | `practical 4.py` | Tower of Hanoi using State Space Search |
| 5 | `practical 5.py` | Blocks World Planning using BFS |
| 6 | `practical 6.py` | 8-Queens using Backtracking Search (CSP) |
| 7 | `practical 7.py` | Rule-Based Chatbot using Pattern Matching |
| 8 | `practical 8.py` | Tic-Tac-Toe using Minimax (Human vs Computer) |

## Requirements

- Python 3.8 or later
- Standard library only (`heapq`, `collections`, `re`, `datetime`); no packages to install

## How to Run

Open a terminal in the repository folder. Because the file names contain a space, put them in quotes:

```bash
python "practical 1.py"
python "practical 2.py"
python "practical 3.py"
python "practical 4.py"
python "practical 5.py"
python "practical 6.py"
python "practical 7.py"     # interactive: type 'bye' to exit
python "practical 8.py"     # interactive: enter cell numbers 1-9
```

On Linux/macOS use `python3` instead of `python` if required.

Practicals 1-6 print their results and finish by themselves. Practicals 7 and 8 first show a demo (7) or start a game (8) and then wait for keyboard input.

## Algorithms Used

1. **Simple Reflex Agent** - Chooses an action (SUCK, LEFT, RIGHT, NO_OP) from condition-action rules applied to the current percept only. Tested on all 8 initial configurations of the two-square world.
2. **Model-Based Agent** - Keeps an internal map of sensed cells, a visited set and a path stack. It prefers unvisited free neighbours closest to the goal (Manhattan distance) and backtracks at dead ends, so it cannot loop. Reports when the goal is unreachable.
3. **A\* Search (8-Puzzle)** - Expands the state with the lowest f(n) = g(n) + h(n) from a priority queue (open list), using Manhattan distance as an admissible heuristic and a closed set of visited states. Unsolvable boards are detected through the parity of inversions.
4. **Tower of Hanoi** - Breadth First Search over the state space of disk arrangements; every legal move is a transition. Finds the minimum of 2^N - 1 moves.
5. **Blocks World** - Breadth First Search over stack configurations with legal moves (move a clear block onto another block or the table) and a visited set, producing a shortest plan.
6. **8-Queens** - Recursive backtracking, one queen per row, checking column and diagonal constraints; undoes a placement when no later row can be completed. Also counts all 92 solutions.
7. **Rule-Based Chatbot** - Ordered list of regular-expression patterns mapped to replies, with exit commands and a default reply for unknown input.
8. **Minimax (Tic-Tac-Toe)** - Full game-tree search; the computer is MAX and the human is MIN. Terminal utilities are +10 / -10 / 0, adjusted by depth so quicker wins are preferred. The computer never loses.

## Repository Structure

```text
AI_Practicals/
├── practical 1.py
├── practical 2.py
├── practical 3.py
├── practical 4.py
├── practical 5.py
├── practical 6.py
├── practical 7.py
├── practical 8.py
└── README.md
```
