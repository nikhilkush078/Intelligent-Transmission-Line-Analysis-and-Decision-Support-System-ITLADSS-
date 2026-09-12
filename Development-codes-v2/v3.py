# ============================================================
# VERSION 3
# Transmission Line Engineering Calculator + Assistant
# ============================================================

import math


# ------------------------------------------------------------
# INPUT PARAMETERS
# ------------------------------------------------------------

line_voltage_kv = 132
frequency_hz = 50
line_length_km = 100
current_a = 200

resistance_per_km = 0.08
inductance_per_km_mh = 0.95
capacitance_per_km_nf = 12

power_factor = 0.9


# ------------------------------------------------------------
# ENGINEERING CALCULATIONS
# ------------------------------------------------------------

def calculate():

    # Total resistance
    R = resistance_per_km * line_length_km

    # Total inductance
    L_mh = inductance_per_km_mh * line_length_km
    L_h = L_mh / 1000

    # Total capacitance
    C_nf = capacitance_per_km_nf * line_length_km
    C_f = C_nf * 1e-9

    # Inductive reactance
    XL = 2 * math.pi * frequency_hz * L_h

    # Capacitive reactance
    if C_f > 0:
        XC = 1 / (2 * math.pi * frequency_hz * C_f)
    else:
        XC = 0

    # Three-phase input power
    voltage_v = line_voltage_kv * 1000

    input_power_w = (
        math.sqrt(3)
        * voltage_v
        * current_a
        * power_factor
    )

    # Three-phase I²R loss
    loss_w = 3 * current_a**2 * R

    # Loss percentage
    loss_percent = (
        loss_w / input_power_w
    ) * 100

    # Output power
    output_power_w = input_power_w - loss_w

    # Efficiency
    efficiency = (
        output_power_w / input_power_w
    ) * 100

    return {
        "resistance": R,
        "inductance_mh": L_mh,
        "capacitance_nf": C_nf,
        "XL": XL,
        "XC": XC,
        "input_power_kw": input_power_w / 1000,
        "loss_kw": loss_w / 1000,
        "loss_percent": loss_percent,
        "efficiency": efficiency
    }


# ------------------------------------------------------------
# CHATBOT
# ------------------------------------------------------------

def assistant(question):

    question = question.lower().strip()

    result = calculate()

    if "voltage" in question:
        return f"Line voltage is {line_voltage_kv} kV."

    elif "frequency" in question:
        return f"Frequency is {frequency_hz} Hz."

    elif "current" in question:
        return f"Line current is {current_a} A."

    elif "length" in question:
        return f"Line length is {line_length_km} km."

    elif "resistance" in question:
        return (
            f"Total line resistance is "
            f"{result['resistance']:.3f} ohm."
        )

    elif "inductance" in question:
        return (
            f"Total line inductance is "
            f"{result['inductance_mh']:.3f} mH."
        )

    elif "capacitance" in question:
        return (
            f"Total line capacitance is "
            f"{result['capacitance_nf']:.3f} nF."
        )

    elif "reactance" in question:

        return (
            f"Inductive reactance XL = "
            f"{result['XL']:.3f} ohm.\n"
            f"Capacitive reactance XC = "
            f"{result['XC']:.3f} ohm."
        )

    elif "loss" in question:

        status = (
            "within"
            if result["loss_percent"] <= 5
            else "above"
        )

        return (
            f"Power loss = {result['loss_kw']:.3f} kW "
            f"({result['loss_percent']:.2f}%).\n"
            f"The loss is {status} the 5% limit."
        )

    elif "efficiency" in question:

        return (
            f"Transmission efficiency is "
            f"{result['efficiency']:.2f}%."
        )

    else:

        return (
            "I can answer questions about voltage, "
            "frequency, current, line length, resistance, "
            "inductance, capacitance, reactance, losses "
            "and efficiency."
        )


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

def display_results():

    result = calculate()

    print("\n" + "=" * 55)
    print(" TRANSMISSION LINE CALCULATION RESULTS")
    print("=" * 55)

    print(f"Voltage        : {line_voltage_kv} kV")
    print(f"Frequency      : {frequency_hz} Hz")
    print(f"Line Length    : {line_length_km} km")
    print(f"Current        : {current_a} A")

    print("-" * 55)

    print(
        f"Resistance     : "
        f"{result['resistance']:.3f} ohm"
    )

    print(
        f"Inductance     : "
        f"{result['inductance_mh']:.3f} mH"
    )

    print(
        f"Capacitance    : "
        f"{result['capacitance_nf']:.3f} nF"
    )

    print(
        f"Inductive XL   : "
        f"{result['XL']:.3f} ohm"
    )

    print(
        f"Capacitive XC  : "
        f"{result['XC']:.3f} ohm"
    )

    print("-" * 55)

    print(
        f"Input Power    : "
        f"{result['input_power_kw']:.2f} kW"
    )

    print(
        f"Power Loss     : "
        f"{result['loss_kw']:.2f} kW"
    )

    print(
        f"Loss Percentage: "
        f"{result['loss_percent']:.2f}%"
    )

    print(
        f"Efficiency     : "
        f"{result['efficiency']:.2f}%"
    )

    print("=" * 55)


display_results()

print("\nAsk the engineering assistant.")
print("Type 'exit' to close.\n")


while True:

    question = input("You: ")

    if question.lower().strip() == "exit":
        print("Assistant: Goodbye!")
        break

    print("\nAssistant:", assistant(question))
    print()