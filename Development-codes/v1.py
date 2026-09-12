question = input("You: ").lower()

if "inductance" in question:
    print("Assistant: Inductance is a property of the transmission line.")

elif "capacitance" in question:
    print("Assistant: Capacitance exists between conductors and ground.")

elif "loss" in question:
    print("Assistant: Transmission line losses occur mainly due to resistance.")

else:
    print("Assistant: I don't understand the question.")