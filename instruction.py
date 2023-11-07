import tkinter as tk
import subprocess

def start_game():
    subprocess.run(["python", "Equation_Explorer.py"], check=True)
    window.destroy()

# Create the Tkinter window
window = tk.Tk()
window.title("Equation Explorer")

# Make the window full screen
window.attributes("-fullscreen", True)

# Load the instruction image
instruction_image = tk.PhotoImage(file="G:\My Drive\Sem 4\TMS2813 (Computational Science Lab)\project\FINALE CSLAB\instruction.png")

# Create a label to display the instruction image
instruction_label = tk.Label(window, image=instruction_image)
instruction_label.pack()

# Create the start button
start_button = tk.Button(window, text="Start", command=start_game)
start_button.pack()

window.mainloop()
