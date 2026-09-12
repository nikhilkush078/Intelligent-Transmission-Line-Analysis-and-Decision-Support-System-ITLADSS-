# ============================================================
# VERSION 2
# Intent Detection + Engineering Response
# ============================================================

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


# ------------------------------------------------------------
# RESPONSE SYSTEM
# ------------------------------------------------------------

def get_response(intent):

    if intent == "INDUCTANCE":
        return "Inductance depends on the transmission-line length and conductor arrangement."

    elif intent == "CAPACITANCE":
        return "Capacitance depends on conductor geometry, spacing and the surrounding medium."

    elif intent == "LOSS":
        return "For a balanced three-phase line, resistive loss can be calculated using P_loss = 3I²R."

    elif intent == "LENGTH_WHAT_IF":
        return "Increasing line length generally increases the total resistance, inductance and capacitance."

    else:
        return "Sorry, I don't understand that question yet."


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

question = input("You: ")

intent = detect_intent(question)

response = get_response(intent)

print("Detected intent:", intent)
print("Assistant:", response)