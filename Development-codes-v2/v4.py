# ============================================================
# VERSION 4
# Rule-Based Engineering Knowledge
# ============================================================

import math


# ------------------------------------------------------------
# SYSTEM PARAMETERS
# ------------------------------------------------------------

line_length_km = 100
frequency_hz = 50
current_a = 200

resistance_per_km = 0.08
inductance_per_km_mh = 0.95
capacitance_per_km_nf = 12


# ------------------------------------------------------------
# ENGINEERING RELATIONSHIPS
# ------------------------------------------------------------

rules = {

    "line length": (
        "Increasing line length generally increases "
        "total resistance, inductance and capacitance."
    ),

    "frequency": (
        "Increasing frequency increases inductive "
        "reactance because XL = 2πfL. "
        "Capacitive reactance decreases because "
        "XC = 1/(2πfC)."
    ),

    "current": (
        "Increasing current increases resistive losses "
        "according to P_loss = 3I²R."
    ),

    "inductance": (
        "Increasing inductance increases inductive "
        "reactance according to XL = 2πfL."
    )
}


# ------------------------------------------------------------
# CALCULATIONS
# ------------------------------------------------------------

def calculate_inductance():

    return (
        inductance_per_km_mh
        * line_length_km
    )


def calculate_resistance():

    return (
        resistance_per_km
        * line_length_km
    )


def calculate_capacitance():

    return (
        capacitance_per_km_nf
        * line_length_km
    )


def calculate_reactance():

    L_h = calculate_inductance() / 1000

    XL = 2 * math.pi * frequency_hz * L_h

    C_f = calculate_capacitance() * 1e-9

    XC = 1 / (
        2 * math.pi
        * frequency_hz
        * C_f
    )

    return XL, XC


# ------------------------------------------------------------
# INTENT DETECTION
# ------------------------------------------------------------

def detect_intent(question):

    question = question.lower()

    if (
        "increase" in question
        and "length" in question
    ):
        return "LENGTH_EFFECT"

    if (
        "increase" in question
        and "frequency" in question
    ):
        return "FREQUENCY_EFFECT"

    if (
        "increase" in question
        and "current" in question
    ):
        return "CURRENT_EFFECT"

    if (
        "increase" in question
        and "inductance" in question
    ):
        return "INDUCTANCE_EFFECT"

    if "inductance" in question:
        return "GET_INDUCTANCE"

    if "resistance" in question:
        return "GET_RESISTANCE"

    if "capacitance" in question:
        return "GET_CAPACITANCE"

    if "reactance" in question:
        return "GET_REACTANCE"

    return "UNKNOWN"


# ------------------------------------------------------------
# ASSISTANT
# ------------------------------------------------------------

def assistant(question):

    intent = detect_intent(question)

    if intent == "LENGTH_EFFECT":
        return rules["line length"]

    elif intent == "FREQUENCY_EFFECT":
        return rules["frequency"]

    elif intent == "CURRENT_EFFECT":
        return rules["current"]

    elif intent == "INDUCTANCE_EFFECT":
        return rules["inductance"]

    elif intent == "GET_INDUCTANCE":

        value = calculate_inductance()

        return (
            f"Total inductance is "
            f"{value:.3f} mH."
        )

    elif intent == "GET_RESISTANCE":

        value = calculate_resistance()

        return (
            f"Total resistance is "
            f"{value:.3f} ohm."
        )

    elif intent == "GET_CAPACITANCE":

        value = calculate_capacitance()

        return (
            f"Total capacitance is "
            f"{value:.3f} nF."
        )

    elif intent == "GET_REACTANCE":

        XL, XC = calculate_reactance()

        return (
            f"Inductive reactance XL = "
            f"{XL:.3f} ohm.\n"
            f"Capacitive reactance XC = "
            f"{XC:.3f} ohm."
        )

    else:

        return (
            "I don't understand that question yet.\n"
            "Try asking about inductance, resistance, "
            "capacitance, reactance, line length, "
            "frequency or current."
        )


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

print("=" * 60)
print(" TRANSMISSION LINE ENGINEERING ASSISTANT - V4")
print("=" * 60)

print("\nCurrent system:")
print(f"Line length : {line_length_km} km")
print(f"Frequency   : {frequency_hz} Hz")
print(f"Current     : {current_a} A")

print("\nExamples:")
print("  What is the inductance?")
print("  What happens if I increase line length?")
print("  What happens if I increase frequency?")
print("  What happens if I increase current?")
print("\nType 'exit' to close.\n")


while True:

    question = input("You: ")

    if question.lower().strip() == "exit":

        print("Assistant: Goodbye!")
        break

    print(
        "Assistant:",
        assistant(question)
    )