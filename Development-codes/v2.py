line_length = 100
inductance = 95
loss = 3.2

question = input("You: ").lower()

if "length" in question:
    print(f"Assistant: The line length is {line_length} km.")

elif "inductance" in question:
    print(f"Assistant: The line inductance is {inductance} mH.")

elif "loss" in question:
    print(f"Assistant: The transmission loss is {loss}%.")