question = input("You: ").lower()

if "increase line length" in question:

    print(
        "Assistant: Increasing line length generally "
        "increases resistance, inductance and capacitance."
    )

elif "increase frequency" in question:

    print(
        "Assistant: Increasing frequency increases "
        "inductive reactance."
    )

elif "increase current" in question:

    print(
        "Assistant: Increasing current increases I²R losses."
    )