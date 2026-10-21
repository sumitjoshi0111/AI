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


# ---------- Reflex agent (condition-action rules) ----------
def reflex_vacuum_agent(percept, world_is_clean):
    """Return an action using only the current percept."""
    location = percept[0]
    status = percept[1]

    if status == "DIRTY":
        return "SUCK"
    if world_is_clean:
        # Nothing more to do; moving around would only lose points.
        return "NO_OP"
    if location == "A":
        return "RIGHT"
    return "LEFT"


# ---------- Environment helpers ----------
def is_world_clean(environment):
    return environment["A"] == "CLEAN" and environment["B"] == "CLEAN"


def show_state(environment, agent_location):
    # Mark the agent's square with brackets
    if agent_location == "A":
        print("   World:  [A:" + environment["A"] + "]   B:" + environment["B"])
    else:
        print("   World:   A:" + environment["A"] + "   [B:" + environment["B"] + "]")


def run_simulation(initial_a, initial_b, start_location, max_steps):
    environment = {"A": initial_a, "B": initial_b}
    agent_location = start_location
    score = 0

    print("Initial state -> A:" + initial_a + ", B:" + initial_b +
          ", Agent at " + start_location)
    print("-" * 60)

    for step in range(1, max_steps + 1):
        percept = (agent_location, environment[agent_location])
        action = reflex_vacuum_agent(percept, is_world_clean(environment))

        print("Step " + str(step) + ": Percept = " + str(percept) +
              "  ->  Action = " + action)

        # Apply the action to the environment
        if action == "SUCK":
            environment[agent_location] = "CLEAN"
            score = score + 10
        elif action == "LEFT":
            agent_location = "A"
            score = score - 1
        elif action == "RIGHT":
            agent_location = "B"
            score = score - 1
        # NO_OP changes nothing

        show_state(environment, agent_location)

        # Stop once everything is clean and the agent has chosen NO_OP
        if action == "NO_OP":
            print("World is clean. Agent stops.")
            break

    print("Final score: " + str(score))
    print("=" * 60)
    return score


# ---------- Main program ----------
if __name__ == "__main__":
    print("SIMPLE REFLEX VACUUM CLEANER AGENT")
    print("Performance: +10 per square cleaned, -1 per move")
    print("=" * 60)

    statuses = ["CLEAN", "DIRTY"]
    locations = ["A", "B"]
    case_number = 1
    total_score = 0

    # Try every possible starting configuration
    for a_status in statuses:
        for b_status in statuses:
            for start in locations:
                print("CASE " + str(case_number))
                total_score = total_score + run_simulation(a_status, b_status, start, 10)
                case_number = case_number + 1

    print("Average score over 8 cases: " + str(total_score / 8))
    print()
    print("Rationality analysis:")
    print("- The agent cleans a dirty square before moving anywhere.")
    print("- It moves only when the current square is clean and work remains.")
    print("- It does NO_OP when everything is clean, so it wastes no points.")
    print("- Limitation: a reflex agent has no memory, so it relies on the")
    print("  environment reporting that the whole world is clean.")
