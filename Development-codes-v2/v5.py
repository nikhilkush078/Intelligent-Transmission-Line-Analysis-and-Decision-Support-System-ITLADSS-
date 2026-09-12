# ============================================================
# VERSION 5
# Transmission Line What-If Analysis
# ============================================================

import math
import re


# ------------------------------------------------------------
# BASE SYSTEM
# ------------------------------------------------------------

system = {

    "length_km": 100,

    "frequency_hz": 50,

    "voltage_kv": 132,

    "current_a": 200,

    "resistance_ohm_km": 0.08,

    "inductance_mh_km": 0.95,

    "capacitance_nf_km": 12,

    "power_factor": 0.9
}


# ------------------------------------------------------------
# ENGINEERING ENGINE
# ------------------------------------------------------------

def calculate(data):

    length = data["length_km"]

    R = (
        data["resistance_ohm_km"]
        * length
    )

    L_mh = (
        data["inductance_mh_km"]
        * length
    )

    L_h = L_mh / 1000

    C_nf = (
        data["capacitance_nf_km"]
        * length
    )

    C_f = C_nf * 1e-9

    XL = (
        2
        * math.pi
        * data["frequency_hz"]
        * L_h
    )

    XC = (
        1
        / (
            2
            * math.pi
            * data["frequency_hz"]
            * C_f
        )
    )

    voltage = data["voltage_kv"] * 1000

    input_power = (
        math.sqrt(3)
        * voltage
        * data["current_a"]
        * data["power_factor"]
    )

    loss = (
        3
        * data["current_a"] ** 2
        * R
    )

    loss_percent = (
        loss / input_power
    ) * 100

    efficiency = (
        (input_power - loss)
        / input_power
    ) * 100

    return {

        "R": R,

        "L_mh": L_mh,

        "C_nf": C_nf,

        "XL": XL,

        "XC": XC,

        "loss_kw": loss / 1000,

        "loss_percent": loss_percent,

        "efficiency": efficiency
    }


# ------------------------------------------------------------
# EXTRACT NEW LENGTH
# ------------------------------------------------------------

def extract_length(question):

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*km",
        question.lower()
    )

    if match:

        return float(
            match.group(1)
        )

    return None


# ------------------------------------------------------------
# WHAT-IF ANALYSIS
# ------------------------------------------------------------

def length_what_if(question):

    new_length = extract_length(question)

    if new_length is None:

        return (
            "Please specify the new length.\n"
            "Example: What happens if I increase "
            "line length to 150 km?"
        )

    if new_length <= 0:

        return "Line length must be greater than zero."

    old_result = calculate(system)

    modified_system = system.copy()

    modified_system["length_km"] = new_length

    new_result = calculate(
        modified_system
    )

    old_length = system["length_km"]

    L_change = (
        (new_result["L_mh"] - old_result["L_mh"])
        / old_result["L_mh"]
    ) * 100

    R_change = (
        (new_result["R"] - old_result["R"])
        / old_result["R"]
    ) * 100

    C_change = (
        (new_result["C_nf"] - old_result["C_nf"])
        / old_result["C_nf"]
    ) * 100

    return (

        "WHAT-IF ANALYSIS\n"
        "----------------------------\n"

        f"Line length:\n"
        f"{old_length} km → {new_length} km\n\n"

        f"Inductance:\n"
        f"{old_result['L_mh']:.3f} mH → "
        f"{new_result['L_mh']:.3f} mH "
        f"({L_change:+.2f}%)\n\n"

        f"Resistance:\n"
        f"{old_result['R']:.3f} Ω → "
        f"{new_result['R']:.3f} Ω "
        f"({R_change:+.2f}%)\n\n"

        f"Capacitance:\n"
        f"{old_result['C_nf']:.3f} nF → "
        f"{new_result['C_nf']:.3f} nF "
        f"({C_change:+.2f}%)\n\n"

        f"Power Loss:\n"
        f"{old_result['loss_percent']:.2f}% → "
        f"{new_result['loss_percent']:.2f}%\n\n"

        f"Efficiency:\n"
        f"{old_result['efficiency']:.2f}% → "
        f"{new_result['efficiency']:.2f}%\n\n"

        "Engineering interpretation:\n"
        "Increasing line length increases the total "
        "series resistance and inductance because "
        "these parameters accumulate along the line. "
        "The total capacitance also increases with "
        "line length."
    )


# ------------------------------------------------------------
# QUESTION PROCESSOR
# ------------------------------------------------------------

def assistant(question):

    question = question.lower()

    if (
        "what happens" in question
        and "length" in question
    ):

        return length_what_if(question)

    elif "inductance" in question:

        result = calculate(system)

        return (
            f"Total inductance is "
            f"{result['L_mh']:.3f} mH."
        )

    elif "resistance" in question:

        result = calculate(system)

        return (
            f"Total resistance is "
            f"{result['R']:.3f} Ω."
        )

    elif "capacitance" in question:

        result = calculate(system)

        return (
            f"Total capacitance is "
            f"{result['C_nf']:.3f} nF."
        )

    elif "loss" in question:

        result = calculate(system)

        return (
            f"Power loss is "
            f"{result['loss_percent']:.2f}%."
        )

    elif "efficiency" in question:

        result = calculate(system)

        return (
            f"Efficiency is "
            f"{result['efficiency']:.2f}%."
        )

    else:

        return (
            "I don't understand that question."
        )


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

print("=" * 65)
print(" TRANSMISSION LINE WHAT-IF ENGINEERING ASSISTANT - V5")
print("=" * 65)

print("\nCurrent line length:")
print(
    f"{system['length_km']} km"
)

print("\nTry:")
print(
    "What happens if I increase line length to 150 km?"
)

print(
    "What is the inductance?"
)

print(
    "What are the losses?"
)

print("\nType 'exit' to close.\n")


while True:

    question = input("You: ")

    if question.lower().strip() == "exit":

        print("Assistant: Goodbye!")
        break

    print("\nAssistant:")
    print(assistant(question))
    print()