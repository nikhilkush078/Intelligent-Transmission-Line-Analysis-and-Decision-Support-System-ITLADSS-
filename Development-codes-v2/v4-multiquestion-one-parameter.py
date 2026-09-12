# ============================================================
# VERSION 4.1
# Multiple Questions - One Parameter
# Parameter: Line Length
# ============================================================

# Current transmission line parameter
line_length_km = 100


# Engineering rule
line_length_rule = (
    "Increasing transmission line length generally increases "
    "total resistance, inductance and capacitance."
)


# ------------------------------------------------------------
# INTENT DETECTION
# ------------------------------------------------------------

def detect_intent(question):

    question = question.lower()

    # Questions asking for the current line length
    if (
        "line length" in question
        or "length of the line" in question
        or "how long is the transmission line" in question
    ):
        # But first check if the question is about increasing length
        if "increase" in question or "increasing" in question:
            return "LENGTH_EFFECT"

        return "GET_LENGTH"

    # Questions asking about the effect of increasing length
    if (
        "increase" in question
        or "increasing" in question
    ) and "length" in question:

        return "LENGTH_EFFECT"

    return "UNKNOWN"


# ------------------------------------------------------------
# ASSISTANT
# ------------------------------------------------------------

def assistant(question):

    intent = detect_intent(question)

    if intent == "GET_LENGTH":

        return (
            f"The current transmission line length "
            f"is {line_length_km} km."
        )

    elif intent == "LENGTH_EFFECT":

        return line_length_rule

    else:

        return (
            "I don't understand that question yet.\n"
            "You can ask about the transmission line length."
        )


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

print("=" * 60)
print(" TRANSMISSION LINE ENGINEERING ASSISTANT")
print(" Multiple Questions - One Parameter")
print("=" * 60)

print(f"\nCurrent line length: {line_length_km} km")

print("\nYou can ask:")
print("1. What is the line length?")
print("2. Tell me the line length.")
print("3. How long is the transmission line?")
print("4. What happens if I increase the line length?")
print("5. What happens when line length increases?")
print("6. Does increasing line length affect resistance?")

print("\nType 'exit' to close.\n")


while True:

    question = input("You: ")

    if question.lower().strip() == "exit":
        print("Assistant: Goodbye!")
        break

    answer = assistant(question)

    print("Assistant:", answer)