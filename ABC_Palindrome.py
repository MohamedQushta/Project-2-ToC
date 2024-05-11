import tkinter as tk
from tkinter import ttk
import json
class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Turing Machine Simulator")

        self.create_widgets()
        self.setup_defaults()

    def create_widgets(self):
        self.input_label = tk.Label(self.master, text="Input String:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_entry = tk.Entry(self.master, width=30)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.run_button = tk.Button(self.master, text="Run", command=self.run_turing_machine)
        self.run_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.step_button = tk.Button(self.master, text="Step", command=self.run_step_once)
        self.step_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_turing_machine)
        self.stop_button.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        self.machine_label = tk.Label(self.master, text="Choose Turing Machine:")
        self.machine_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.machine_var = tk.StringVar()
        self.machine_dropdown = ttk.Combobox(self.master, textvariable=self.machine_var, state="readonly")
        self.machine_dropdown['values'] = ("Palindrome Machine", "ABC Machine", "Other")
        self.machine_dropdown.current(1)  # Default to ABC Machine
        self.machine_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.tape_canvas = tk.Canvas(self.master, width=600, height=100, bg="white")
        self.tape_canvas.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

        # Binding for dropdown selection
        self.machine_dropdown.bind("<<ComboboxSelected>>", self.select_turing_machine)

    def setup_defaults(self):
        self.tape_length = 30
        self.cell_width = 20
        self.cell_height = 50
        self.tape_cells = []
        self.pointer = None
        self.select_turing_machine()

    def select_turing_machine(self, event=None):
        selected_machine = self.machine_var.get()
        if selected_machine == "Palindrome Machine":
            self.tm = palindrome_machine()
        elif selected_machine == "ABC Machine":
            self.tm = ABC_TuringMachine()
        elif selected_machine == "Other":
            self.tm = FlexibleTM()
        else:
            raise ValueError("Invalid Turing Machine selected")

    def draw_tape(self):
        self.tape_canvas.delete("all")
        tape = self.tm.tape
        tape_width = len(tape) * self.cell_width
        start_x = (self.tape_canvas.winfo_width() - tape_width) / 2
        
        for i, symbol in enumerate(tape):
            x0 = start_x + i * self.cell_width
            x1 = x0 + self.cell_width
            y0 = self.cell_height / 2
            y1 = y0 + self.cell_height
            self.tape_canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="lightgray")
            self.tape_canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=symbol)
        
        self.pointer = self.tape_canvas.create_line(start_x + self.tm.tape_index * self.cell_width + self.cell_width / 2, 0,
                                                     start_x + self.tm.tape_index * self.cell_width + self.cell_width / 2, self.cell_height,
                                                     fill="red", width=2)

    def run_turing_machine(self):
        input_str = self.input_entry.get().strip()
        if not input_str:
            return
        self.tm.input_str = input_str
        self.tm.reset()
        self.status_label.config(text="")  # Reset status label
        self.run_step()

    def run_step(self):
        if self.tm.state not in ['accept', 'reject']:
            self.tm.step()
            self.draw_tape()
            self.step_id = self.master.after(500, self.run_step)
        else:
            result = "Accepted" if self.tm.state == 'accept' else "Rejected"
            if result == "Accepted":
                self.status_label.config(text="Accepted", fg="green")
            else:
                self.status_label.config(text="Rejected", fg="red")

    def run_step_once(self):
        if self.tm.state not in ['accept', 'reject']:
            self.tm.step()
            self.draw_tape()
            if self.tm.state in ['accept', 'reject']:
                result = "Accepted" if self.tm.state == 'accept' else "Rejected"
                if result == "Accepted":
                    self.status_label.config(text="Accepted", fg="green")
                else:
                    self.status_label.config(text="Rejected", fg="red")

    def stop_turing_machine(self):
        if hasattr(self, 'step_id'):
            self.master.after_cancel(self.step_id)
class TuringMachine:
    def step(self):
        current_symbol = self.tape[self.tape_index]
        transition = self.transition_table[self.state].get(current_symbol)
        if transition:
            if 'write' in transition:
                self.tape[self.tape_index] = transition['write']
            if 'move' in transition:
                if transition['move'] == 'L':
                    self.tape_index -= 1
                    if self.tape_index < 0:
                        self.tape.insert(0, ' ')
                        self.tape_index = 0
                elif transition['move'] == 'R':
                    self.tape_index += 1
                    if self.tape_index >= len(self.tape):
                        self.tape.append(' ')
            if 'next_state' in transition:
                self.state = transition['next_state']
        else:
            self.state = 'reject'

    def reset(self):
        self.tape = list(self.input_str)
        self.tape_index = 0
        self.state = 'start'

class palindrome_machine(TuringMachine):
    def __init__(self):
        with open('palindrome.json', 'r') as file:
            data = json.load(file)
        self.transition_table = data

    

class ABC_TuringMachine(TuringMachine):
    def __init__(self):
        with open('ABC.json', 'r') as file:
            data = json.load(file)
        self.transition_table = data

class FlexibleTM(TuringMachine):
    def __init__(self):
        with open('other.json', 'r') as file:
            data = json.load(file)
        self.transition_table = data
def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
