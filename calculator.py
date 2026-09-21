



import tkinter as tk

window = tk.Tk()
window.title("Calculator")


display_value = tk.StringVar(value="0")

display = tk.Label(window, textvariable=display_value)
display.grid(row=0, column=0, columnspan=3)

def press_number(number):
    current_value = display_value.get()

    if current_value == "0":
        display_value.set(str(number))
    else:
        display_value.set(current_value + str(number))

buttton_zero = tk.Button(window, text="0", command=lambda: press_number(0))
buttton_zero.grid(row=4, column=0)

buttton_one = tk.Button(window, text="1", command=lambda: press_number(1))
buttton_one.grid(row=3, column=0)

buttton_two = tk.Button(window, text="2", command=lambda: press_number(2))
buttton_two.grid(row=3, column=1)

buttton_three = tk.Button(window, text="3", command=lambda: press_number(3))
buttton_three.grid(row=3, column=2)

buttton_four = tk.Button(window, text="4", command=lambda: press_number(4))
buttton_four.grid(row=2, column=0)

buttton_five = tk.Button(window, text="5", command=lambda: press_number(5))
buttton_five.grid(row=2, column=1)


buttton_six = tk.Button(window, text="6", command=lambda: press_number(6))
buttton_six.grid(row=2, column=2)


buttton_seven = tk.Button(window, text="7", command=lambda: press_number(7))
buttton_seven.grid(row=1, column=0)

buttton_eight = tk.Button(window, text="8", command=lambda: press_number(8))
buttton_eight.grid(row=1, column=1)

buttton_nine = tk.Button(window, text="9", command=lambda: press_number(9))
buttton_nine.grid(row=1, column=2)





                            
window.mainloop()



