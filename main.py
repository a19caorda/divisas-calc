from tkinter import Tk, StringVar, OptionMenu, RIGHT, LEFT, BOTTOM, Button, Frame, DoubleVar, messagebox, Label
from tkinter.ttk import Entry
import requests

tk = Tk()
tk.title("Calculadora de divisas")

CURRENCIES = [
    "EUR", "USD", "JPY", "CNY", "PHP"
]

cur = StringVar(tk)
Entry(master=tk, textvariable=cur).grid(row=0, column=0, columnspan=2)

from_cur = StringVar(tk)
from_cur.set(CURRENCIES[0])

to_cur = StringVar(tk)
to_cur.set(CURRENCIES[1])

OptionMenu(tk, from_cur, *CURRENCIES).grid(row=1, column=0)
OptionMenu(tk, to_cur, *CURRENCIES).grid(row=1, column=1)


def numberButtons(i):
    return lambda: cur.set(cur.get() + str(i))


def submit():
    if from_cur.get() == to_cur.get():
        rate = 1
    else:
        url = f"https://api.exchangeratesapi.io/latest?base={from_cur.get()}&symbols={to_cur.get()}"
        res = requests.get(url)
        rate = res.json()['rates'][to_cur.get()]
    f = float(cur.get()) * float(rate)
    result.set(f"Result: {f:.2f}")


subFrame = Frame(tk)
for i in range(9):
    Button(subFrame, text=f"{i+1}", command=numberButtons(1+i)).grid(row=int(i/3), column=i % 3)

Button(subFrame, text=f"{0}", command=numberButtons(0)).grid(row=3, column=0)
Button(subFrame, text=f",", command=numberButtons(".")).grid(row=3, column=1)
Button(subFrame, text=f">", command=submit).grid(row=3, column=2)

subFrame.grid(columnspan=2)

result = StringVar(tk)
Label(tk, textvariable=result).grid(column=0, row=4, columnspan=2)

tk.mainloop()
