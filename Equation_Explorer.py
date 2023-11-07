from tkinter import *
import tkinter as tk
from tkinter import messagebox
import random
import csv
import subprocess


dark_grey = "#777b7d"
yellow = "#c9b458"
green = "#6aaa64"
light_grey = "#d3d6da"
white = "#ffffff"
black = "#000000"

# Run the script to generate equations
subprocess.run(["python", "generateEqn.py"])

class RiddleGame:
    def __init__(self, master):
        self.master = master
        
        # Initialize entry boxes and tries
        self.entry_boxes = []
        self.tries = 6

        self.create_riddle_ui()
        
    def read_riddles(self, file_path):
        riddles = []
        with open(file_path, 'r', encoding='utf-8') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            next(reader)  # Skip the header row
            for row in reader:
                equation_type = int(row[0])
                riddle = row[1]
                riddles.append((equation_type, riddle))
        return riddles

    def read_equations(self, equation_file_path):
        equations = []
        with open(equation_file_path, 'r', encoding='utf-8') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            next(reader)  # Skip the header row
            for row in reader:
                equation_type = int(row[0])
                equation = row[1]
                hints = row[2]
                solution = row[3]
                equations.append((equation_type, equation, hints, solution))
        return equations

    def select_random_row(self, filtered_row):
        return random.choice(filtered_row)
    
    def get_type(self, selected_row):
        selected_type = selected_row[0]
        return selected_type

    def get_equation(self, selected_row):
        selected_equation = selected_row[1]
        return selected_equation

    def get_hint(self, selected_row):
        selected_hint = selected_row[2]
        return selected_hint

    def get_solution(self, selected_row):
        selected_solution = selected_row[3]
        return selected_solution

    def calculate_equation_length(self, selected_equation):
        selected_equation = selected_equation.replace(" ", "")
        equation_len = len(selected_equation)
        return equation_len

    # --------------------------------Part 1 of the Game--------------------------------
    def create_riddle_ui(self):
        if hasattr(self, 'equation_type_label'):
            self.equation_type_label.destroy()

         # Read the riddles from the TSV file
        self.riddles = self.read_riddles('riddle.tsv')
        self.row = self.read_equations('equations.tsv')

        # Select a random riddle
        self.selected_riddle = random.choice(self.riddles)

        # Filter the row by equation type
        self.filtered_row = [eq for eq in self.row if eq[0] == self.selected_riddle[0]]

        # Select a random equation from the filtered list
        self.selected_row = self.select_random_row(self.filtered_row)
        self.selected_type = self.get_type(self.selected_row)
        self.selected_equation = self.get_equation(self.selected_row)
        self.selected_hint = self.get_hint(self.selected_row)
        self.selected_solution = self.get_solution(self.selected_row)

        # Calculate equation length
        self.selected_equation_len = self.calculate_equation_length(self.selected_equation)
        
        self.riddle_label = Label(self.master, text=self.selected_riddle[1], font=("Arial", 18), wraplength=400)
        self.riddle_label.pack(pady=20)

        self.selected_answer = StringVar()

        self.option_1 = Radiobutton(self.master, text="Linear Algebra", variable=self.selected_answer, value="1")
        self.option_1.pack(pady=5)

        self.option_2 = Radiobutton(self.master, text="Quadratic Function", variable=self.selected_answer, value="2")
        self.option_2.pack(pady=5)

        self.option_3 = Radiobutton(self.master, text="Cubic Function", variable=self.selected_answer, value="3")
        self.option_3.pack(pady=5)

        self.submit_button = Button(self.master, text="Submit", padx=10, pady=5, command=self.check_answer)
        self.submit_button.pack(pady=10)

    def check_answer(self):
        user_answer = self.selected_answer.get()
        correct_answer = str(self.selected_riddle[0])

        if user_answer == correct_answer:
            self.clear_riddle_screen()
            self.display_message("Congratulations! You got it right!")
            self.next_button = Button(self.master, text="Next", padx=10, pady=5, command=self.correctly_guessed)
            self.next_button.pack(pady=10)
        else:
            self.clear_riddle_screen()
            self.display_message("Oops! You guessed wrong.")
            self.try_again_button = Button(self.master, text="Try Again", padx=10, pady=5, command=self.reset_game_riddle)
            self.try_again_button.pack(pady=10)

    def display_message(self, message):
        self.message_label = Label(self.master, text=message, font=("Arial", 16))
        self.message_label.pack(pady=20)

    def clear_riddle_screen(self):
        self.riddle_label.destroy()
        self.option_1.destroy()
        self.option_2.destroy()
        self.option_3.destroy()
        self.submit_button.destroy()
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        if hasattr(self, 'try_again_button'):
            self.try_again_button.destroy()

    def reset_game_riddle(self):
        self.clear_riddle_screen()
        # Select a random riddle after the game resets
        self.selected_riddle = random.choice(self.riddles)
        self.create_riddle_ui()

    def correctly_guessed(self):
        self.clear_riddle_screen()
        self.next_button.destroy()
        self.create_equation_ui()

    # --------------------------------Part 2 of the Game--------------------------------
    def create_equation_ui(self):
        # Get the equation type of the selected equation
        equation_type = self.selected_row[0]
        print(self.selected_equation)
        # Map equation types to their corresponding descriptions
        equation_type_descriptions = {
            1: "Linear Algebra",
            2: "Quadratic Function",
            3: "Cubic Function",
        }

        # Get the description for the equation type
        equation_type_description = equation_type_descriptions.get(equation_type, "Unknown Equation Type")

        # Create a label widget to display the equation type description
        self.equation_type_label = Label(self.master, text="Equation Type: {}".format(equation_type_description),font=("Arial", 16))
        self.equation_type_label.pack(pady=20)
        
        self.hints_label = Label(self.master, text=f"Hints : {self.selected_hint}", font=("Arial", 18))
        self.hints_label.pack(pady=10)
        
        equation_len = self.selected_equation_len

        # Clear the entry boxes from previous attempts
        for box in self.entry_boxes:
            box.destroy()

        self.entry_boxes = []

        def validate_input(char):
            if len(char) == 0:  # Allow empty input (for backspace)
                return True
            if len(char) > 1:  # Allow only one character
                return False
            return True

        def on_validate(event):
            entry_index = self.entry_boxes.index(event.widget)
            if entry_index < len(self.entry_boxes) - 1:  # Move cursor to the next entry box
                self.entry_boxes[entry_index + 1].focus_set()

        def on_backspace(event):
            entry_index = self.entry_boxes.index(event.widget)
            if entry_index > 0 and not event.widget.get():  # Move cursor to the previous entry box if empty
                self.entry_boxes[entry_index - 1].focus_set()

        for _ in range(6):
            self.row_frame = Frame(self.master)
            self.row_frame.pack()

            for i in range(equation_len):
                validate_cmd = (self.row_frame.register(validate_input), '%P')
                box = Entry(self.row_frame, font=("Arial", 15), width=3, validate='key',
                            validatecommand=validate_cmd)
                box.pack(side=LEFT, padx=5, pady=10)
                box.bind('<Return>', on_validate)
                box.bind('<BackSpace>', on_backspace)
                self.entry_boxes.append(box)

        self.tries_label = Label(self.master, text="Tries: {}".format(self.tries), font=("Arial", 16))
        self.tries_label.pack(pady=20)

        self.submit_button = Button(self.master, text="Submit Guess", padx=10, pady=5, command=self.check_guess)
        self.submit_button.pack(pady=10)

    def check_guess(self):
        # Destroy the message label
        self.message_label.destroy()

        # Remove spaces from the solution
        equation = str(self.selected_equation)
        correct_equation = equation.replace(" ", "")

        # Get the user's guess from the entry boxes row by row
        guess_rows = [] 
        current_row = []
        for i, box in enumerate(self.entry_boxes, 1):
            current_row.append(box.get())
            if i % self.selected_equation_len == 0:
                guess_rows.append("".join(current_row))
                current_row = []

        # Provide feedback by changing the colors of the entry boxes
        for i, guess_row in enumerate(guess_rows):
            for j, letter in enumerate(guess_row):
                if letter.lower() == correct_equation[j].lower():
                    # Correct letter in the correct position (colored box)
                    self.entry_boxes[i * self.selected_equation_len + j].config(bg="green", fg="white")
                elif letter.lower() in correct_equation.lower():
                    # Correct letter in the wrong position (different colored box)
                    self.entry_boxes[i * self.selected_equation_len + j].config(bg="yellow", fg="black")
                else:
                    # Incorrect letter (empty box)
                    self.entry_boxes[i * self.selected_equation_len + j].config(bg="grey", fg="white")

        # Check if any row matches the correct equation
        if any(guess.lower() == correct_equation.lower() for guess in guess_rows):
            self.clear_equation_screen()
            self.display_message("Congratulations! You guessed the equation correctly!")
            self.next_button_equation = Button(self.master, text="Next", padx=10, pady=5, command=self.correctly_guessed_equation)
            self.next_button_equation.pack(pady=10)
        else:
            self.tries -= 1
            if self.tries == 0:
                self.clear_equation_screen()
                self.display_message("Sorry, you ran out of tries. The correct equation was: {}".format(equation))
                self.try_again_button = Button(self.master, text="Try Again", padx=10, pady=5, command=self.reset_game_riddle)
                self.try_again_button.pack(pady=10) 
            else:
                self.display_message("Incorrect guess. {} tries remaining.".format(self.tries))

    def display_message(self, message):
        self.message_label = Label(self.master, text=message, font=("Arial", 16))
        self.message_label.pack(pady=20)

    def clear_equation_screen(self):
        #self.equation_label.destroy()
        for box in self.entry_boxes:
            box.destroy()
        self.tries_label.destroy()
        self.row_frame.destroy()
        self.submit_button.destroy()
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        if hasattr(self, 'try_again_button'):
            self.try_again_button.destroy()

    def reset_game_riddle(self):
        self.clear_riddle_screen()
        # Select a random riddle after the game resets
        self.selected_riddle = random.choice(self.riddles)
        self.create_riddle_ui()

    def correctly_guessed_equation(self):
        self.clear_equation_screen()
        self.next_button_equation.destroy()
        self.create_solve_ui()
    
    # --------------------------------Part 3 of the Game--------------------------------
    def create_solve_ui(self):
        
        self.x_values = self.get_x(self.selected_solution)
        print(self.x_values)
        self.score = 5
        
        if self.selected_type == 1:
            self.y_value = self.get_y(self.selected_solution)
            solve_label = Label(self.master, text="Solve this equation, where y = {}".format(self.y_value), font=("Arial", 16))
            solve_label.pack(pady=20)
        else:
            solve_label = Label(self.master, text="Solve this equation", font=("Arial", 16))
            solve_label.pack(pady=20)
        
        self.equation_label = Label(self.master, text=self.selected_equation, font=("Arial", 18))
        self.equation_label.pack(pady=10)
        
        self.solution_entry = Entry(self.master, font=("Arial", 14))
        self.solution_entry.pack(pady=5)
        
        self.check_button = Button(self.master, text="Check", font=("Arial", 14), command=self.check_solution)
        self.check_button.pack(pady=5)
        
        self.score_label = Label(self.master, text="Score: {}".format(self.score), font=("Arial", 14))
        self.score_label.pack(pady=10)
        
    def check_solution(self):
        user_solution = self.solution_entry.get()

        if user_solution == "":
            messagebox.showwarning("Invalid Input", "Please enter a solution for x.")
        else:
            if self.selected_type == 1:
                if user_solution in str(self.x_values):
                    messagebox.showinfo("Correct", "Your solution is correct! Thanks for playing :)")
                    root.quit()
                else:
                    messagebox.showinfo("Wrong", f"Wrong! The correct answer is x = {self.x_values}")
                    
            else:
                if user_solution in str(self.x_values):
                    messagebox.showinfo("Correct", "Your solution is correct! Thanks for playing :)")
                    root.quit()
                else:
                    messagebox.showinfo("Wrong", f"Wrong! The correct answer is x = {' or '.join(str(x) for x in self.x_values)}")
                    

            #if self.current_equation < len(self.equations):
            #    self.display_equation()
            #else:
            #    messagebox.showinfo("Game Over", f"Game over! Your final score is {self.score}/{len(self.equations)}")
            #    self.root.destroy()

    def get_x(self, solution):
        parts = solution.split(',')
        if self.selected_type == 1:
            # Iterate over the parts to find the one containing 'x'
            for part in parts:
                # Strip whitespace from the part
                stripped_part = part.strip()
                # Check if the part starts with 'y ='
                if stripped_part.startswith('x ='):
                    # Extract the value after the equals sign
                    x_value1 = stripped_part.split('= ')[1].strip()
            return x_value1 # Return a list with a single value
        elif self.selected_type == 2:
            x_value2 = [int(x.strip()) for x in parts[:2]]
            print(x_value2)
            return x_value2 # Return the first two values as a list
        elif self.selected_type == 3:
            x_value3 = [int(x.strip()) for x in parts[:3]]
            print(x_value3)
            return x_value3# Return the first three values as a list
        else:
            return []  # Return an empty list for other types

    def get_y(self, solution):
        # Split the text by commas
        parts = solution.split(',')

        # Iterate over the parts to find the one containing 'y'
        for part in parts:
            # Strip whitespace from the part
            stripped_part = part.strip()

            # Check if the part starts with 'y ='
            if stripped_part.startswith('y ='):
                # Extract the value after the equals sign
                value = stripped_part.split('= ')[1].strip()

                # Return the value as an integer
                return int(value)

        # If 'y' is not found, return None
        return None
        

# Create the main application windowf
root = Tk()
root.title("Equation Explorer")

s_width = root.winfo_screenwidth()
s_height = root.winfo_screenheight()

#root['background'] = 'white'
# Set the dimensions of the window
root.geometry(f"{s_width}x{s_height}")


game = RiddleGame(root)

root.mainloop()
