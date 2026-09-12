import tkinter as tk
from tkinter import ttk, messagebox
import math
import re


# ============================================================
# TRANSMISSION LINE ENGINE
# ============================================================

def calculate_line(data):
    """
    Simplified medium transmission-line calculations.

    Inputs:
        voltage_kv
        frequency_hz
        length_km
        current_a
        resistance_ohm_km
        inductance_mh_km
        capacitance_nf_km
        power_factor

    Returns calculated electrical parameters.
    """

    V_ll = data["voltage_kv"] * 1000
    f = data["frequency_hz"]
    length = data["length_km"]
    current = data["current_a"]
    R_per_km = data["resistance_ohm_km"]
    L_per_km = data["inductance_mh_km"] / 1000
    C_per_km = data["capacitance_nf_km"] * 1e-9
    pf = data["power_factor"]

    # Total line parameters
    R_total = R_per_km * length
    L_total = L_per_km * length
    C_total = C_per_km * length

    # Reactances
    XL_total = 2 * math.pi * f * L_total
    XC_total = 1 / (2 * math.pi * f * C_total) if C_total > 0 else 0

    # 3-phase input power
    input_power = math.sqrt(3) * V_ll * current * pf

    # Copper/resistive loss
    loss_watts = 3 * current**2 * R_total

    loss_kw = loss_watts / 1000

    # Percentage loss
    loss_percent = (loss_watts / input_power) * 100 if input_power > 0 else 0

    # Output power
    output_power = input_power - loss_watts

    # Efficiency
    efficiency = (
        (output_power / input_power) * 100
        if input_power > 0
        else 0
    )

    # Approximate voltage drop
    sin_phi = math.sqrt(max(0, 1 - pf**2))

    voltage_drop = math.sqrt(3) * current * (
        R_total * pf + XL_total * sin_phi
    )

    voltage_regulation = (
        voltage_drop / V_ll * 100
        if V_ll > 0
        else 0
    )

    # Simple Ferranti indication:
    # Long/high-voltage lines are more susceptible.
    ferranti = (
        length >= 100 and
        data["voltage_kv"] >= 132 and
        C_total > 0
    )

    return {
        "R_total": R_total,
        "L_total": L_total,
        "C_total": C_total,
        "XL_total": XL_total,
        "XC_total": XC_total,
        "input_power_kw": input_power / 1000,
        "loss_kw": loss_kw,
        "loss_percent": loss_percent,
        "output_power_kw": output_power / 1000,
        "efficiency": efficiency,
        "voltage_drop": voltage_drop,
        "voltage_regulation": voltage_regulation,
        "ferranti": ferranti
    }


# ============================================================
# RULE DATABASE
# ============================================================

RELATIONSHIPS = {

    "line_length": {
        "inductance": "increases",
        "capacitance": "increases",
        "resistance": "increases",
        "reactance": "increases",
        "losses": "generally increase"
    },

    "frequency": {
        "inductive_reactance": "increases",
        "capacitive_reactance": "decreases"
    },

    "inductance": {
        "inductive_reactance": "increases"
    },

    "current": {
        "losses": "increase significantly",
        "voltage_drop": "increases"
    },

    "resistance": {
        "losses": "increase"
    },

    "voltage": {
        "current_for_same_power": "generally decreases",
        "losses_for_same_power": "generally decrease"
    }
}


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(question):

    q = question.lower().strip()

    # --------------------------------------------------------
    # WHAT-IF QUESTIONS
    # --------------------------------------------------------

    if (
        ("increase" in q or "decrease" in q or "change" in q)
        and
        ("length" in q or "distance" in q)
    ):
        return "WHAT_IF_LENGTH"

    if (
        ("increase" in q or "decrease" in q or "change" in q)
        and
        ("voltage" in q)
    ):
        return "WHAT_IF_VOLTAGE"

    if (
        ("increase" in q or "decrease" in q or "change" in q)
        and
        ("frequency" in q)
    ):
        return "WHAT_IF_FREQUENCY"

    if (
        ("increase" in q or "decrease" in q or "change" in q)
        and
        ("current" in q)
    ):
        return "WHAT_IF_CURRENT"

    if (
        ("increase" in q or "decrease" in q or "change" in q)
        and
        ("inductance" in q)
    ):
        return "WHAT_IF_INDUCTANCE"

    # --------------------------------------------------------
    # DIRECT PARAMETERS
    # --------------------------------------------------------

    if "inductance" in q:
        return "GET_INDUCTANCE"

    if "capacitance" in q:
        return "GET_CAPACITANCE"

    if "resistance" in q:
        return "GET_RESISTANCE"

    if "reactance" in q:
        return "GET_REACTANCE"

    if "loss" in q or "losses" in q:
        return "GET_LOSS"

    if "efficiency" in q:
        return "GET_EFFICIENCY"

    if "ferranti" in q:
        return "GET_FERRANTI"

    if "voltage regulation" in q or "regulation" in q:
        return "GET_REGULATION"

    if "line length" in q or "distance" in q:
        return "GET_LENGTH"

    if "frequency" in q:
        return "GET_FREQUENCY"

    if "current" in q:
        return "GET_CURRENT"

    if "voltage" in q:
        return "GET_VOLTAGE"

    if "help" in q:
        return "HELP"

    if q in ["hi", "hello", "hey"]:
        return "GREETING"

    return "UNKNOWN"


# ============================================================
# VALUE EXTRACTION
# ============================================================

def extract_number(question):

    match = re.search(
        r"([-+]?\d*\.?\d+)",
        question
    )

    if match:
        return float(match.group(1))

    return None


# ============================================================
# CHATBOT
# ============================================================

def chatbot(question, current_data):

    intent = detect_intent(question)

    result = calculate_line(current_data)

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if intent == "GREETING":

        return (
            "Hello! I am your Transmission Line Engineering "
            "Assistant.\n\n"
            "You can ask me about inductance, capacitance, "
            "losses, efficiency, voltage regulation, Ferranti "
            "effect, or what-if conditions."
        )

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if intent == "HELP":

        return (
            "You can ask questions such as:\n\n"
            "• What is the line inductance?\n"
            "• What are the losses?\n"
            "• What is the efficiency?\n"
            "• Is the loss below 5%?\n"
            "• What happens if I increase line length?\n"
            "• What happens if I increase current?\n"
            "• What happens if I increase frequency?\n"
            "• What happens if I increase inductance?"
        )

    # --------------------------------------------------------
    # DIRECT QUESTIONS
    # --------------------------------------------------------

    if intent == "GET_INDUCTANCE":

        return (
            f"The total line inductance is "
            f"{result['L_total']:.6f} H "
            f"({result['L_total'] * 1000:.3f} mH)."
        )

    if intent == "GET_CAPACITANCE":

        return (
            f"The total line capacitance is "
            f"{result['C_total']:.9f} F "
            f"({result['C_total'] * 1e6:.3f} µF)."
        )

    if intent == "GET_RESISTANCE":

        return (
            f"The total line resistance is "
            f"{result['R_total']:.3f} Ω."
        )

    if intent == "GET_REACTANCE":

        return (
            f"Total inductive reactance XL = "
            f"{result['XL_total']:.3f} Ω.\n\n"
            f"Total capacitive reactance XC = "
            f"{result['XC_total']:.3f} Ω."
        )

    if intent == "GET_LOSS":

        status = (
            "within"
            if result["loss_percent"] <= 5
            else "above"
        )

        return (
            f"The calculated power loss is "
            f"{result['loss_kw']:.3f} kW "
            f"({result['loss_percent']:.2f}%).\n\n"
            f"The loss is {status} the 5% limit."
        )

    if intent == "GET_EFFICIENCY":

        return (
            f"The calculated transmission efficiency is "
            f"{result['efficiency']:.2f}%."
        )

    if intent == "GET_FERRANTI":

        if result["ferranti"]:
            return (
                "The present line conditions indicate that "
                "Ferranti-effect analysis may be important. "
                "It becomes particularly significant for "
                "long, lightly loaded, high-voltage lines."
            )

        return (
            "Under the present simplified model, strong "
            "Ferranti-effect conditions are not indicated."
        )

    if intent == "GET_REGULATION":

        return (
            f"The approximate voltage regulation is "
            f"{result['voltage_regulation']:.2f}%."
        )

    if intent == "GET_LENGTH":

        return (
            f"The current transmission-line length is "
            f"{current_data['length_km']:.2f} km."
        )

    if intent == "GET_FREQUENCY":

        return (
            f"The current operating frequency is "
            f"{current_data['frequency_hz']:.2f} Hz."
        )

    if intent == "GET_CURRENT":

        return (
            f"The current operating current is "
            f"{current_data['current_a']:.2f} A."
        )

    if intent == "GET_VOLTAGE":

        return (
            f"The current line voltage is "
            f"{current_data['voltage_kv']:.2f} kV."
        )

    # --------------------------------------------------------
    # WHAT-IF: LINE LENGTH
    # --------------------------------------------------------

    if intent == "WHAT_IF_LENGTH":

        old_value = current_data["length_km"]

        number = extract_number(question)

        if number is not None:
            new_value = number
        else:
            if "increase" in question.lower():
                new_value = old_value * 1.10
            else:
                new_value = old_value * 0.90

        if new_value <= 0:
            return "The new line length must be greater than zero."

        modified = current_data.copy()
        modified["length_km"] = new_value

        old_result = calculate_line(current_data)
        new_result = calculate_line(modified)

        return compare_results(
            "line length",
            old_value,
            new_value,
            "km",
            old_result,
            new_result
        )

    # --------------------------------------------------------
    # WHAT-IF: VOLTAGE
    # --------------------------------------------------------

    if intent == "WHAT_IF_VOLTAGE":

        old_value = current_data["voltage_kv"]

        number = extract_number(question)

        if number is not None:
            new_value = number
        else:
            if "increase" in question.lower():
                new_value = old_value * 1.10
            else:
                new_value = old_value * 0.90

        if new_value <= 0:
            return "The new voltage must be greater than zero."

        modified = current_data.copy()
        modified["voltage_kv"] = new_value

        old_result = calculate_line(current_data)
        new_result = calculate_line(modified)

        return compare_results(
            "voltage",
            old_value,
            new_value,
            "kV",
            old_result,
            new_result
        )

    # --------------------------------------------------------
    # WHAT-IF: FREQUENCY
    # --------------------------------------------------------

    if intent == "WHAT_IF_FREQUENCY":

        old_value = current_data["frequency_hz"]

        number = extract_number(question)

        if number is not None:
            new_value = number
        else:
            if "increase" in question.lower():
                new_value = old_value * 1.10
            else:
                new_value = old_value * 0.90

        if new_value <= 0:
            return "The new frequency must be greater than zero."

        modified = current_data.copy()
        modified["frequency_hz"] = new_value

        old_result = calculate_line(current_data)
        new_result = calculate_line(modified)

        return compare_results(
            "frequency",
            old_value,
            new_value,
            "Hz",
            old_result,
            new_result
        )

    # --------------------------------------------------------
    # WHAT-IF: CURRENT
    # --------------------------------------------------------

    if intent == "WHAT_IF_CURRENT":

        old_value = current_data["current_a"]

        number = extract_number(question)

        if number is not None:
            new_value = number
        else:
            if "increase" in question.lower():
                new_value = old_value * 1.10
            else:
                new_value = old_value * 0.90

        if new_value <= 0:
            return "The new current must be greater than zero."

        modified = current_data.copy()
        modified["current_a"] = new_value

        old_result = calculate_line(current_data)
        new_result = calculate_line(modified)

        return compare_results(
            "current",
            old_value,
            new_value,
            "A",
            old_result,
            new_result
        )

    # --------------------------------------------------------
    # WHAT-IF: INDUCTANCE
    # --------------------------------------------------------

    if intent == "WHAT_IF_INDUCTANCE":

        old_value = current_data["inductance_mh_km"]

        number = extract_number(question)

        if number is not None:
            new_value = number
        else:
            if "increase" in question.lower():
                new_value = old_value * 1.10
            else:
                new_value = old_value * 0.90

        if new_value <= 0:
            return "The new inductance must be greater than zero."

        modified = current_data.copy()
        modified["inductance_mh_km"] = new_value

        old_result = calculate_line(current_data)
        new_result = calculate_line(modified)

        return compare_results(
            "inductance per km",
            old_value,
            new_value,
            "mH/km",
            old_result,
            new_result
        )

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    return (
        "I could not identify that question.\n\n"
        "Try asking about:\n"
        "• inductance\n"
        "• capacitance\n"
        "• resistance\n"
        "• losses\n"
        "• efficiency\n"
        "• voltage regulation\n"
        "• Ferranti effect\n"
        "• what happens if I increase line length?"
    )


# ============================================================
# COMPARISON ENGINE
# ============================================================

def percentage_change(old, new):

    if old == 0:
        return 0

    return ((new - old) / abs(old)) * 100


def compare_results(
    parameter,
    old_value,
    new_value,
    unit,
    old_result,
    new_result
):

    L_change = percentage_change(
        old_result["L_total"],
        new_result["L_total"]
    )

    C_change = percentage_change(
        old_result["C_total"],
        new_result["C_total"]
    )

    R_change = percentage_change(
        old_result["R_total"],
        new_result["R_total"]
    )

    loss_change = percentage_change(
        old_result["loss_percent"],
        new_result["loss_percent"]
    )

    efficiency_change = (
        new_result["efficiency"]
        - old_result["efficiency"]
    )

    XL_change = percentage_change(
        old_result["XL_total"],
        new_result["XL_total"]
    )

    response = (
        f"WHAT-IF ANALYSIS\n"
        f"-----------------------------\n"
        f"{parameter.title()}: "
        f"{old_value:.3f} {unit} → "
        f"{new_value:.3f} {unit}\n\n"
    )

    response += (
        f"Total Inductance:\n"
        f"  {old_result['L_total'] * 1000:.4f} mH → "
        f"{new_result['L_total'] * 1000:.4f} mH "
        f"({L_change:+.2f}%)\n\n"
    )

    response += (
        f"Total Capacitance:\n"
        f"  {old_result['C_total'] * 1e6:.4f} µF → "
        f"{new_result['C_total'] * 1e6:.4f} µF "
        f"({C_change:+.2f}%)\n\n"
    )

    response += (
        f"Total Resistance:\n"
        f"  {old_result['R_total']:.4f} Ω → "
        f"{new_result['R_total']:.4f} Ω "
        f"({R_change:+.2f}%)\n\n"
    )

    response += (
        f"Inductive Reactance:\n"
        f"  {old_result['XL_total']:.4f} Ω → "
        f"{new_result['XL_total']:.4f} Ω "
        f"({XL_change:+.2f}%)\n\n"
    )

    response += (
        f"Power Loss:\n"
        f"  {old_result['loss_percent']:.3f}% → "
        f"{new_result['loss_percent']:.3f}% "
        f"({loss_change:+.2f}%)\n\n"
    )

    response += (
        f"Efficiency:\n"
        f"  {old_result['efficiency']:.3f}% → "
        f"{new_result['efficiency']:.3f}% "
        f"({efficiency_change:+.3f} percentage points)\n\n"
    )

    response += "Engineering interpretation:\n"

    if parameter == "line length":

        response += (
            "Increasing line length increases the total "
            "series resistance and inductance because these "
            "parameters accumulate along the transmission line. "
            "The total capacitance also increases with line "
            "length. Under the same operating conditions, "
            "longer lines generally experience greater losses "
            "and voltage-drop effects."
        )

    elif parameter == "frequency":

        response += (
            "Inductive reactance follows XL = 2πfL, so "
            "increasing frequency increases inductive reactance. "
            "Capacitive reactance follows XC = 1/(2πfC), so "
            "it decreases as frequency increases."
        )

    elif parameter == "current":

        response += (
            "The resistive power loss follows P_loss = 3I²R "
            "for a balanced three-phase line. Therefore, "
            "increasing current can increase copper losses "
            "approximately with the square of current."
        )

    elif parameter == "inductance per km":

        response += (
            "Inductive reactance follows XL = 2πfL. "
            "Therefore, increasing line inductance increases "
            "the inductive reactance when frequency remains "
            "constant."
        )

    elif parameter == "voltage":

        response += (
            "For a fixed current, changing voltage changes "
            "the transmitted power. In a constant-power "
            "transmission system, higher voltage generally "
            "allows lower current, which can reduce I²R losses."
        )

    return response


# ============================================================
# GUI APPLICATION
# ============================================================

class TransmissionLineApp:

    def __init__(self, root):

        self.root = root
        self.root.title(
            "Intelligent Transmission Line Analysis System"
        )

        self.root.geometry("1200x750")

        self.create_variables()
        self.create_gui()

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    def create_variables(self):

        self.voltage_var = tk.StringVar(value="132")
        self.frequency_var = tk.StringVar(value="50")
        self.length_var = tk.StringVar(value="100")
        self.current_var = tk.StringVar(value="200")
        self.resistance_var = tk.StringVar(value="0.08")
        self.inductance_var = tk.StringVar(value="0.95")
        self.capacitance_var = tk.StringVar(value="0.012")
        self.pf_var = tk.StringVar(value="0.9")

    # --------------------------------------------------------
    # GUI
    # --------------------------------------------------------

    def create_gui(self):

        title = tk.Label(
            self.root,
            text="TRANSMISSION LINE ANALYSIS & ENGINEERING ASSISTANT",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=15)

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=15)

        # ====================================================
        # LEFT SIDE - INPUT
        # ====================================================

        input_frame = tk.LabelFrame(
            main,
            text="Transmission Line Inputs",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        input_frame.pack(
            side="left",
            fill="y",
            padx=10
        )

        self.add_input(
            input_frame,
            "Voltage (kV)",
            self.voltage_var,
            0
        )

        self.add_input(
            input_frame,
            "Frequency (Hz)",
            self.frequency_var,
            1
        )

        self.add_input(
            input_frame,
            "Line Length (km)",
            self.length_var,
            2
        )

        self.add_input(
            input_frame,
            "Current (A)",
            self.current_var,
            3
        )

        self.add_input(
            input_frame,
            "Resistance (Ω/km)",
            self.resistance_var,
            4
        )

        self.add_input(
            input_frame,
            "Inductance (mH/km)",
            self.inductance_var,
            5
        )

        self.add_input(
            input_frame,
            "Capacitance (nF/km)",
            self.capacitance_var,
            6
        )

        self.add_input(
            input_frame,
            "Power Factor",
            self.pf_var,
            7
        )

        calculate_button = tk.Button(
            input_frame,
            text="CALCULATE",
            command=self.calculate,
            font=("Arial", 11, "bold"),
            height=2
        )

        calculate_button.grid(
            row=8,
            column=0,
            columnspan=2,
            pady=20,
            sticky="ew"
        )

        # ====================================================
        # CENTER - RESULTS
        # ====================================================

        result_frame = tk.LabelFrame(
            main,
            text="Analysis Results",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )

        result_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.result_text = tk.Text(
            result_frame,
            font=("Consolas", 11),
            wrap="word"
        )

        self.result_text.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # RIGHT - CHATBOT
        # ====================================================

        chatbot_frame = tk.LabelFrame(
            main,
            text="Engineering Assistant",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )

        chatbot_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10
        )

        self.chat_text = tk.Text(
            chatbot_frame,
            font=("Arial", 10),
            wrap="word"
        )

        self.chat_text.pack(
            fill="both",
            expand=True
        )

        chat_bottom = tk.Frame(chatbot_frame)
        chat_bottom.pack(fill="x", pady=5)

        self.question_entry = tk.Entry(
            chat_bottom,
            font=("Arial", 10)
        )

        self.question_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.question_entry.bind(
            "<Return>",
            lambda event: self.ask_question()
        )

        ask_button = tk.Button(
            chat_bottom,
            text="Ask",
            command=self.ask_question
        )

        ask_button.pack(side="right")

        self.chat_text.insert(
            "end",
            "Assistant: Hello! Enter your transmission-line "
            "parameters and ask me an engineering question.\n\n"
        )

    # --------------------------------------------------------
    # ADD INPUT
    # --------------------------------------------------------

    def add_input(
        self,
        parent,
        label,
        variable,
        row
    ):

        tk.Label(
            parent,
            text=label,
            font=("Arial", 10)
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=7
        )

        tk.Entry(
            parent,
            textvariable=variable,
            width=15
        ).grid(
            row=row,
            column=1,
            padx=10,
            pady=7
        )

    # --------------------------------------------------------
    # GET CURRENT DATA
    # --------------------------------------------------------

    def get_data(self):

        try:

            data = {
                "voltage_kv":
                    float(self.voltage_var.get()),

                "frequency_hz":
                    float(self.frequency_var.get()),

                "length_km":
                    float(self.length_var.get()),

                "current_a":
                    float(self.current_var.get()),

                "resistance_ohm_km":
                    float(self.resistance_var.get()),

                "inductance_mh_km":
                    float(self.inductance_var.get()),

                "capacitance_nf_km":
                    float(self.capacitance_var.get()),

                "power_factor":
                    float(self.pf_var.get())
            }

            if data["voltage_kv"] <= 0:
                raise ValueError

            if data["frequency_hz"] <= 0:
                raise ValueError

            if data["length_km"] <= 0:
                raise ValueError

            if data["current_a"] <= 0:
                raise ValueError

            if not 0 < data["power_factor"] <= 1:
                raise ValueError

            return data

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid positive numerical values.\n\n"
                "Power factor must be between 0 and 1."
            )

            return None

    # --------------------------------------------------------
    # CALCULATE
    # --------------------------------------------------------

    def calculate(self):

        data = self.get_data()

        if data is None:
            return

        result = calculate_line(data)

        self.result_text.delete(
            "1.0",
            "end"
        )

        self.result_text.insert(
            "end",
            "TRANSMISSION LINE RESULTS\n"
            "====================================\n\n"
        )

        self.result_text.insert(
            "end",
            f"Line Length       : "
            f"{data['length_km']:.2f} km\n"
        )

        self.result_text.insert(
            "end",
            f"Voltage           : "
            f"{data['voltage_kv']:.2f} kV\n"
        )

        self.result_text.insert(
            "end",
            f"Frequency         : "
            f"{data['frequency_hz']:.2f} Hz\n"
        )

        self.result_text.insert(
            "end",
            f"Current           : "
            f"{data['current_a']:.2f} A\n\n"
        )

        self.result_text.insert(
            "end",
            "------------------------------------\n"
        )

        self.result_text.insert(
            "end",
            f"Total Resistance  : "
            f"{result['R_total']:.4f} Ω\n"
        )

        self.result_text.insert(
            "end",
            f"Total Inductance  : "
            f"{result['L_total'] * 1000:.4f} mH\n"
        )

        self.result_text.insert(
            "end",
            f"Total Capacitance : "
            f"{result['C_total'] * 1e6:.4f} µF\n"
        )

        self.result_text.insert(
            "end",
            f"Inductive XL      : "
            f"{result['XL_total']:.4f} Ω\n"
        )

        self.result_text.insert(
            "end",
            f"Capacitive XC     : "
            f"{result['XC_total']:.4f} Ω\n\n"
        )

        self.result_text.insert(
            "end",
            "------------------------------------\n"
        )

        self.result_text.insert(
            "end",
            f"Input Power       : "
            f"{result['input_power_kw']:.3f} kW\n"
        )

        self.result_text.insert(
            "end",
            f"Power Loss        : "
            f"{result['loss_kw']:.3f} kW\n"
        )

        self.result_text.insert(
            "end",
            f"Loss Percentage   : "
            f"{result['loss_percent']:.3f}%\n"
        )

        self.result_text.insert(
            "end",
            f"Efficiency        : "
            f"{result['efficiency']:.3f}%\n"
        )

        self.result_text.insert(
            "end",
            f"Voltage Regulation: "
            f"{result['voltage_regulation']:.3f}%\n\n"
        )

        if result["loss_percent"] <= 5:

            self.result_text.insert(
                "end",
                "✓ LOSS STATUS: WITHIN 5% LIMIT\n"
            )

        else:

            self.result_text.insert(
                "end",
                "⚠ LOSS STATUS: ABOVE 5% LIMIT\n"
            )

        if result["ferranti"]:

            self.result_text.insert(
                "end",
                "\nFerranti Effect: POTENTIALLY SIGNIFICANT\n"
            )

        else:

            self.result_text.insert(
                "end",
                "\nFerranti Effect: NOT STRONGLY INDICATED\n"
            )

    # --------------------------------------------------------
    # ASK QUESTION
    # --------------------------------------------------------

    def ask_question(self):

        question = self.question_entry.get().strip()

        if not question:
            return

        data = self.get_data()

        if data is None:
            return

        answer = chatbot(
            question,
            data
        )

        self.chat_text.insert(
            "end",
            f"\nYou: {question}\n"
        )

        self.chat_text.insert(
            "end",
            f"Assistant: {answer}\n"
        )

        self.chat_text.see("end")

        self.question_entry.delete(
            0,
            "end"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TransmissionLineApp(root)

    root.mainloop()