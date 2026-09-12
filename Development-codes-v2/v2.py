# ============================================================
# VERSION 2
# Dynamic Transmission Line Parameters
# ============================================================

line_length = 100          # km
resistance_per_km = 0.08   # ohm/km
inductance_per_km = 0.95   # mH/km


def calculate_resistance():
    return line_length * resistance_per_km


def calculate_inductance():
    return line_length * inductance_per_km


def assistant(question):

    question = question.lower().strip()

    if "line length" in question or "distance" in question:
        return f"Line length is {line_length} km."

    elif "resistance" in question:
        resistance = calculate_resistance()

        return (
            f"Total line resistance is "
            f"{resistance:.3f} ohm."
        )

    elif "inductance" in question:
        inductance = calculate_inductance()

        return (
            f"Total line inductance is "
            f"{inductance:.3f} mH."
        )

    else:
        return (
            "I can answer questions about "
            "line length, resistance and inductance."
        )


print("=" * 55)
print(" TRANSMISSION LINE ENGINEERING ASSISTANT - V2")
print("=" * 55)
print("Available parameters:")
print("• Line length")
print("• Resistance")
print("• Inductance")
print("Type 'exit' to close.\n")


while True:

    question = input("You: ")

    if question.lower().strip() == "exit":
        print("Assistant: Goodbye!")
        break

    print("Assistant:", assistant(question))