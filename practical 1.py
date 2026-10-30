# ============================================================
# Practical Number : 1
# Practical Title  : Simple Reflex Agent for the Vacuum Cleaner World
#
# Aim:
#   To design and implement a simple reflex agent for the two-location
#   vacuum cleaner world and to analyze its rational behavior.
#
# Theory:
#   An agent perceives its environment through sensors and acts on it
#   through actuators. A simple reflex agent chooses its action only
#   from the CURRENT percept, using condition-action rules. It keeps no
#   memory of the past. In the vacuum world there are two locations,
#   A and B, and each can be Clean or Dirty. The percept is the pair
#   (location, status). The actions are SUCK, LEFT, RIGHT and NO_OP.
#   An agent is rational if it picks the action that maximizes its
#   performance measure. Here the performance measure is: +10 for every
#   dirty square cleaned and -1 for every move (LEFT or RIGHT).
#   The agent is rational because it never moves when the current square
#   is dirty, and it stops (NO_OP) once the world is clean.
#
# Algorithm:
#   1. Create the environment: status of A and B, and agent location.
#   2. Get the percept (location, status of that location).
#   3. Apply the rules:
#        - If status is DIRTY            -> SUCK
#        - Else if location is A         -> RIGHT
#        - Else if location is B         -> LEFT
#      (If both squares are known clean, the environment tells us the
#       task is finished and the agent does NO_OP.)
#   4. Execute the action and update the environment and score.
#   5. Display the state and the action.
#   6. Repeat for a fixed number of steps for every initial state.
#
# Expected Outcome:
#   For all 8 possible initial configurations (4 dirt combinations x
#   2 start locations) the agent cleans both squares and then does
#   NO_OP. The score and number of steps are printed for each case.
# ============================================================



# Simple Reflex Vacuum Cleaner Agent

def vacuum_agent(location, status):
    if status == "DIRTY":
        return "SUCK"
    elif location == "A":
        return "RIGHT"
    else:
        return "LEFT"


def main():
    environment = {"A": "DIRTY", "B": "DIRTY"}
    location = "A"

    while True:
        # Stop when both rooms are clean
        if environment["A"] == "CLEAN" and environment["B"] == "CLEAN":
            print("Both rooms are clean. STOP")
            break

        status = environment[location]
        action = vacuum_agent(location, status)

        print("Location:", location, "Action:", action)

        if action == "SUCK":
            environment[location] = "CLEAN"
        elif action == "RIGHT":
            location = "B"
        else:
            location = "A"

    print("Final Environment:", environment)


if __name__ == "__main__":
    main()
