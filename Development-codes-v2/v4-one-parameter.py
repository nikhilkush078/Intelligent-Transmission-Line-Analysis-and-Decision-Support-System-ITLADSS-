
# ============================================================
# SIMPLE VERSION 4
# Rule-Based Engineering Assistant
# Parameter: Line Length
# ============================================================


# ------------------------------------------------------------
# SYSTEM PARAMETER
# ------------------------------------------------------------

line_length_km = 100


# ------------------------------------------------------------
# ENGINEERING RULE
# ------------------------------------------------------------

line_length_rule = (
    "If transmission line length increases, "
    "total resistance, inductance and capacitance "
    "generally increase."
)


# ------------------------------------------------------------
# INTENT DETECTION
# ------------------------------------------------------------

def detect_intent(question):

    question = question.lower()

    if "increase" in question and "length" in question:
        return "LENGTH_EFFECT"

    if "length" in question:
        return "GET_LENGTH"

    return "UNKNOWN"


# ------------------------------------------------------------
# ASSISTANT
# ------------------------------------------------------------

def assistant(question):

    intent = detect_intent(question)

    if intent == "GET_LENGTH":

        return f"Current transmission line length is {line_length_km} km."

    elif intent == "LENGTH_EFFECT":

        return line_length_rule

    else:

        return (
            "I only understand questions about "
            "transmission line length."
        )


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

print("=" * 50)
print(" SIMPLE TRANSMISSION LINE ASSISTANT")
print("=" * 50)

print(f"\nCurrent line length: {line_length_km} km")

print("\nTry asking:")
print("1. What is the line length?")
print("2. What happens if I increase line length?")

print("\nType 'exit' to close.\n")


while True:

    question = input("You: ")

    if question.lower().strip() == "exit":
        print("Assistant: Goodbye!")
        break

    answer = assistant(question)

    print("Assistant:", answer)

