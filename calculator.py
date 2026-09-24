import math
import tkinter as tk
from tkinter import messagebox


class CalculatorApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Calculator")
        self.window.geometry("760x650")
        self.window.minsize(650, 550)
        self.window.configure(bg="#121212")

        # Calculator state
        self.stored_number = None
        self.operator = None
        self.waiting_for_number = False
        self.error_active = False

        # Display variables
        self.display_value = tk.StringVar(value="0")
        self.expression_value = tk.StringVar(value="")

        self.create_layout()
        self.bind_keys()

    def create_layout(self):
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(1, weight=2)

        calculator_frame = tk.Frame(
            self.window,
            bg="#121212",
            padx=18,
            pady=18
        )
        calculator_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        history_frame = tk.Frame(
            self.window,
            bg="#1e1e1e",
            padx=15,
            pady=15
        )
        history_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        calculator_frame.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1,
            uniform="buttons"
        )

        calculator_frame.grid_rowconfigure(1, weight=2)

        for row in range(2, 8):
            calculator_frame.grid_rowconfigure(row, weight=1)

        self.create_display(calculator_frame)
        self.create_buttons(calculator_frame)
        self.create_history(history_frame)

    def create_display(self, parent):
        title = tk.Label(
            parent,
            text="CALCULATOR",
            font=("Segoe UI", 12, "bold"),
            fg="#ff9500",
            bg="#121212"
        )
        title.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 10)
        )

        display_frame = tk.Frame(
            parent,
            bg="#1e1e1e",
            padx=15,
            pady=15
        )
        display_frame.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="nsew",
            pady=(0, 15)
        )

        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(1, weight=1)

        expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_value,
            font=("Segoe UI", 13),
            fg="#999999",
            bg="#1e1e1e",
            anchor="e"
        )
        expression_label.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        display_label = tk.Label(
            display_frame,
            textvariable=self.display_value,
            font=("Segoe UI", 34, "bold"),
            fg="white",
            bg="#1e1e1e",
            anchor="e"
        )
        display_label.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    def create_buttons(self, parent):
        buttons = [
            ("C", 2, 0, self.clear, "special"),
            ("⌫", 2, 1, self.backspace, "special"),
            ("%", 2, 2, self.percentage, "special"),
            ("÷", 2, 3, lambda: self.choose_operator("÷"), "operator"),

            ("√", 3, 0, self.square_root, "special"),
            ("x²", 3, 1, self.square, "special"),
            ("1/x", 3, 2, self.reciprocal, "special"),
            ("×", 3, 3, lambda: self.choose_operator("×"), "operator"),

            ("7", 4, 0, lambda: self.enter_number("7"), "number"),
            ("8", 4, 1, lambda: self.enter_number("8"), "number"),
            ("9", 4, 2, lambda: self.enter_number("9"), "number"),
            ("−", 4, 3, lambda: self.choose_operator("−"), "operator"),

            ("4", 5, 0, lambda: self.enter_number("4"), "number"),
            ("5", 5, 1, lambda: self.enter_number("5"), "number"),
            ("6", 5, 2, lambda: self.enter_number("6"), "number"),
            ("+", 5, 3, lambda: self.choose_operator("+"), "operator"),

            ("1", 6, 0, lambda: self.enter_number("1"), "number"),
            ("2", 6, 1, lambda: self.enter_number("2"), "number"),
            ("3", 6, 2, lambda: self.enter_number("3"), "number"),

            ("±", 7, 0, self.toggle_sign, "number"),
            ("0", 7, 1, lambda: self.enter_number("0"), "number"),
            (".", 7, 2, self.enter_decimal, "number"),
        ]

        for text, row, column, command, button_type in buttons:
            self.make_button(
                parent,
                text,
                row,
                column,
                command,
                button_type
            )

        equals_button = tk.Button(
            parent,
            text="=",
            command=self.calculate,
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#ff9500",
            activebackground="#e68600",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        equals_button.grid(
            row=6,
            column=3,
            rowspan=2,
            sticky="nsew",
            padx=4,
            pady=4
        )

    def make_button(
        self,
        parent,
        text,
        row,
        column,
        command,
        button_type
    ):
        colours = {
            "number": ("#2d2d2d", "#3a3a3a", "white"),
            "operator": ("#ff9500", "#e68600", "white"),
            "special": ("#505050", "#606060", "white")
        }

        background, active_background, foreground = colours[button_type]

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 17, "bold"),
            fg=foreground,
            bg=background,
            activebackground=active_background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        button.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=4,
            pady=4
        )

    def create_history(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        heading = tk.Label(
            parent,
            text="HISTORY",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        heading.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.history_list = tk.Listbox(
            parent,
            font=("Consolas", 12),
            fg="#dddddd",
            bg="#252525",
            selectbackground="#ff9500",
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.history_list.grid(row=1, column=0, sticky="nsew")

        clear_history_button = tk.Button(
            parent,
            text="Clear history",
            command=self.clear_history,
            font=("Segoe UI", 11),
            fg="white",
            bg="#3a3a3a",
            activebackground="#505050",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        clear_history_button.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(10, 0)
        )

    def enter_number(self, number):
        if self.error_active or self.waiting_for_number:
            self.display_value.set(number)
            self.waiting_for_number = False
            self.error_active = False
            return

        current = self.display_value.get()

        if current == "0":
            self.display_value.set(number)
        elif len(current) < 16:
            self.display_value.set(current + number)

    def enter_decimal(self):
        if self.error_active or self.waiting_for_number:
            self.display_value.set("0.")
            self.waiting_for_number = False
            self.error_active = False
            return

        if "." not in self.display_value.get():
            self.display_value.set(self.display_value.get() + ".")

    def choose_operator(self, operator):
        if self.error_active:
            return

        if self.operator is not None and not self.waiting_for_number:
            self.calculate()

        self.stored_number = float(self.display_value.get())
        self.operator = operator
        self.waiting_for_number = True

        self.expression_value.set(
            f"{self.format_number(self.stored_number)} {operator}"
        )

    def calculate(self):
        if (
            self.operator is None
            or self.stored_number is None
            or self.error_active
        ):
            return

        second_number = float(self.display_value.get())
        first_number = self.stored_number
        operator = self.operator

        try:
            if operator == "+":
                result = first_number + second_number
            elif operator == "−":
                result = first_number - second_number
            elif operator == "×":
                result = first_number * second_number
            elif operator == "÷":
                if second_number == 0:
                    raise ZeroDivisionError
                result = first_number / second_number
            else:
                return

            calculation = (
                f"{self.format_number(first_number)} "
                f"{operator} "
                f"{self.format_number(second_number)} = "
                f"{self.format_number(result)}"
            )

            self.history_list.insert(0, calculation)
            self.display_value.set(self.format_number(result))
            self.expression_value.set(calculation)

        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")

        except OverflowError:
            self.show_error("Number is too large")

        self.operator = None
        self.stored_number = None
        self.waiting_for_number = True

    def clear(self):
        self.display_value.set("0")
        self.expression_value.set("")
        self.stored_number = None
        self.operator = None
        self.waiting_for_number = False
        self.error_active = False

    def backspace(self):
        if self.waiting_for_number or self.error_active:
            return

        current = self.display_value.get()

        if len(current) > 1:
            self.display_value.set(current[:-1])
        else:
            self.display_value.set("0")

    def toggle_sign(self):
        if self.error_active:
            return

        value = float(self.display_value.get())
        self.display_value.set(self.format_number(-value))

    def percentage(self):
        if self.error_active:
            return

        value = float(self.display_value.get())
        result = value / 100
        self.display_value.set(self.format_number(result))

    def square_root(self):
        if self.error_active:
            return

        value = float(self.display_value.get())

        if value < 0:
            self.show_error("Cannot square-root a negative number")
            return

        result = math.sqrt(value)
        self.record_unary_calculation(f"√{self.format_number(value)}", result)

    def square(self):
        if self.error_active:
            return

        value = float(self.display_value.get())
        result = value ** 2
        self.record_unary_calculation(
            f"({self.format_number(value)})²",
            result
        )

    def reciprocal(self):
        if self.error_active:
            return

        value = float(self.display_value.get())

        if value == 0:
            self.show_error("Cannot divide by zero")
            return

        result = 1 / value
        self.record_unary_calculation(
            f"1/{self.format_number(value)}",
            result
        )

    def record_unary_calculation(self, expression, result):
        calculation = f"{expression} = {self.format_number(result)}"

        self.display_value.set(self.format_number(result))
        self.expression_value.set(calculation)
        self.history_list.insert(0, calculation)
        self.waiting_for_number = True

    def show_error(self, message):
        self.display_value.set("Error")
        self.expression_value.set(message)
        self.error_active = True
        self.waiting_for_number = True

        messagebox.showerror("Calculator Error", message)

    def clear_history(self):
        self.history_list.delete(0, tk.END)

    def format_number(self, number):
        if number == int(number):
            return str(int(number))

        return f"{number:.10g}"

    def bind_keys(self):
        self.window.bind("<Key>", self.handle_key)

    def handle_key(self, event):
        key = event.char
        key_name = event.keysym

        if key.isdigit():
            self.enter_number(key)
        elif key == ".":
            self.enter_decimal()
        elif key == "+":
            self.choose_operator("+")
        elif key == "-":
            self.choose_operator("−")
        elif key == "*":
            self.choose_operator("×")
        elif key == "/":
            self.choose_operator("÷")
        elif key == "%":
            self.percentage()
        elif key_name in ("Return", "KP_Enter"):
            self.calculate()
        elif key_name == "BackSpace":
            self.backspace()
        elif key_name in ("Escape", "Delete"):
            self.clear()


window = tk.Tk()
app = CalculatorApp(window)
window.mainloop()

