# ============================================================
# VERSION 1
# Basic Rule-Based Transmission Line Assistant
# ============================================================

LINE_LENGTH = 100  # km


def assistant(question):
    question = question.lower().strip()

    if "line length" in question:
        return f"The current transmission line length is {LINE_LENGTH} km."

    else:
        return "Sorry, I can only answer questions about line length."


print("=" * 50)
print(" TRANSMISSION LINE ENGINEERING ASSISTANT")
print("=" * 50)
print("Type 'exit' to close the program.\n")

while True:

    question = input("You: ")

    if question.lower().strip() == "exit":
        print("Assistant: Goodbye!")
        break

    answer = assistant(question)

    print("Assistant:", answer)