line_length = 100

def detect_intent(question):
    words = question.lower()

    if "length" in words and "increase" in words:
        return "LENGTH_WHAT_IF"

    if "length" in words:
        return "LENGTH"

    return "UNKNOWN"


question = input("You: ")

intent = detect_intent(question)

if intent == "LENGTH_WHAT_IF":
    print("Increasing line length affects the transmission line parameters.")

elif intent == "LENGTH":
    print(f"Line length is {line_length} km.")

else:
    print("Unknown question.")