import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.title("calc")
root.geometry("300x500")


# ボタンがクリックされたときの動作(メッセージボックス表示)
def button_click(e):
    btn = e.widget
    txt = btn["text"]
    entry.insert(tk.END, txt)

# テキスト入力欄追加
entry = tk.Entry(justify="right", width=10, font=40)
entry.grid(row=0, column=0, columnspan=3)

# 数字ボタン配置
for i in range(10):
    button = tk.Button(root, text=i, width=4, height=2, font=30)
    button.bind("<1>", button_click)
    button.grid(row=(12-i) // 3, column=(12-i) % 3)


# +ボタン追加
button = tk.Button(root, text="+", width=4, height=2, font=30)
button.bind("<1>", button_click)
button.grid(row=4, column=1)

# =ボタン追加
button = tk.Button(root, text="=", width=4, height=2, font=30)
button.grid(row=4, column=2)

root.mainloop()
