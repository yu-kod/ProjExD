import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.title("calc")
root.geometry("300x500")


def button_click(e):
    btn = e.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"{txt}のボタンが押されました")


for i in range(9, -1, -1):
    button = tk.Button(root, text=i, width=4, height=2, font=30)
    button.bind("<1>", button_click)
    button.grid(row=i // 3, column=i % 3)

root.mainloop()
