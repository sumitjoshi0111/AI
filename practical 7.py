# ============================================================
# Practical Number : 7
# Practical Title  : Rule-Based Chatbot using Pattern Matching
#
# Aim:
#   To develop a simple chatbot that replies to the user with the help
#   of predefined rules and pattern matching.
#
# Theory:
#   A rule-based chatbot does not learn from data. Its knowledge is a
#   list of RULES written by the programmer. Each rule has a PATTERN
#   (what the user may say) and a RESPONSE (what the bot should answer).
#   The user's sentence is converted to lower case and compared with
#   each pattern in order. Patterns are written as regular expressions
#   using Python's built-in "re" module, so a rule like "hi|hello|hey"
#   matches any of those words. The first rule that matches decides the
#   reply. If no rule matches, a DEFAULT response is given. Such bots
#   (like the early program ELIZA) are easy to build and explain, but
#   they cannot understand meaning outside their rules.
#
# Algorithm:
#   1. Define the list of rules: (pattern, reply).
#   2. Show a short demo with sample inputs.
#   3. Read a sentence typed by the user.
#   4. Convert the sentence to lower case and remove extra spaces.
#   5. If it matches an exit pattern (bye / exit / quit), say goodbye
#      and stop.
#   6. Check the rules one by one; on the first match print its reply.
#   7. If no rule matches, print the default reply.
#   8. Go back to step 3.
#
# Expected Outcome:
#   The bot greets the user, answers basic questions (name, how are you,
#   time, what is AI), remembers the user's name, replies with a
#   default message to unknown input, and ends on an exit command.
# ============================================================

import re
from datetime import datetime

# Each rule: (regular expression pattern, reply text)
# {0} in a reply is replaced by the text captured inside ( ) in the pattern.
RULES = [
    (r"my name is (\w+)", "Nice to meet you, {0}! How can I help you?"),
    (r"\bhow are you\b", "I am just a program, but I am working fine. Thank you for asking!"),
    (r"\b(your name|who are you)\b", "I am PyBot, a simple rule-based chatbot."),
    (r"what is (ai|artificial intelligence)", "Artificial Intelligence is the study of making machines act intelligently."),
    (r"\b(what can you do|help)\b", "I can greet you, tell the time, and answer a few basic questions about AI."),
    (r"\bsearch\b", "Search algorithms such as BFS, DFS and A* explore states to find a solution."),
    (r"\b(thanks|thank you)\b", "You are welcome!"),
    (r"\b(hi|hello|hey|good morning|good evening)\b", "Hello! How can I help you today?"),
]

EXIT_PATTERN = r"\b(bye|goodbye|exit|quit)\b"
DEFAULT_REPLY = "Sorry, I did not understand that. Try saying 'help'."


def get_reply(user_text):
    """Return (reply, stop_flag) for one line typed by the user."""
    text = user_text.lower().strip()

    if text == "":
        return "Please type something.", False

    # Exit commands
    if re.search(EXIT_PATTERN, text):
        return "Goodbye! Have a nice day.", True

    # Special rule: asking for the time (answer depends on the clock)
    if re.search(r"\btime\b", text):
        return "The current time is " + datetime.now().strftime("%H:%M") + ".", False

    # Try every rule in order
    for pattern, reply in RULES:
        match = re.search(pattern, text)
        if match:
            if "{0}" in reply:
                name = match.group(1).capitalize()
                reply = reply.replace("{0}", name)
            return reply, False

    # No rule matched
    return DEFAULT_REPLY, False


def run_demo():
    print("--- Demo with sample inputs ---")
    sample_inputs = [
        "Hello",
        "My name is Sumit",
        "How are you?",
        "What is your name?",
        "What is AI?",
        "Tell me a joke",
        "bye",
    ]
    for sentence in sample_inputs:
        reply, stop = get_reply(sentence)
        print("You    : " + sentence)
        print("PyBot  : " + reply)
        if stop:
            break
    print("--- End of demo ---")


def chat():
    print("PyBot: Hi! I am PyBot. Type 'bye', 'exit' or 'quit' to end the chat.")
    while True:
        try:
            user_text = input("You   : ")
        except EOFError:                # input stream closed (e.g. no keyboard)
            print()
            print("PyBot: Input ended. Goodbye!")
            break
        reply, stop = get_reply(user_text)
        print("PyBot : " + reply)
        if stop:
            break


# ---------- Main program ----------
if __name__ == "__main__":
    print("RULE-BASED CHATBOT")
    print("=" * 60)
    run_demo()
    print("=" * 60)
    print("Now you can chat with the bot yourself.")
    chat()
