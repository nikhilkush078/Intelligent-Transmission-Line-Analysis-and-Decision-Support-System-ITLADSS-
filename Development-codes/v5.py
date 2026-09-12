def detect_intent(question):

    question = question.lower()

    if "inductance" in question:
        return "INDUCTANCE"

    if "capacitance" in question:
        return "CAPACITANCE"

    if "loss" in question:
        return "LOSS"

    if "increase" in question and "length" in question:
        return "LENGTH_WHAT_IF"

    return "UNKNOWN"


question = input("You: ")

intent = detect_intent(question)

print("Detected intent:", intent)