"""電卓のGUIの設定と実行"""

import tkinter as tk
from input_handler import handle_input, CalculatorState
from functools import partial

root = tk.Tk()
root.title("電卓")

screen = tk.StringVar()
entry = tk.Entry(root, textvariable=screen, font=("Arial", 20), justify="right", state="readonly", takefocus=0)
entry.grid(row=0, column=0, columnspan=5)

state = CalculatorState()

# ラッパー関数の定義
def handle_click(event):
    text = event.widget.cget("text") 
    if hasattr(event.widget, "cget"):
        pass
    else:
        "="
    handle_input(text, screen, state)

def handle_key(event, screen, state):
    key = event.char
    allowed_chars = "0123456789+-*/().%"
    
    if event.keysym == "Return":
        handle_input("=", screen, state)
    elif event.keysym == "BackSpace":
        screen.set(screen.get()[:-1])
        state.just_evaluated = False
    elif key in allowed_chars:
        handle_input(key, screen, state)
    else:
        return

# partialで引数を固定した関数を作成
bound_handle_key = partial(handle_key, screen=screen, state=state)

root.bind("<Key>", bound_handle_key)

# ボタンの設定 (右上２つは空きボタン)
buttons = [
    "√", "±", "", "",
    "(", ")", "%", "C",
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+",
]

# ボタンの作成・配置の設定
row, col = 1, 0
for button in buttons:
    btn = tk.Button(root, text=button, font="Arial 15", width=5, height=2)
    btn.grid(row=row, column=col)
    btn.bind("<Button-1>", handle_click)
    col += 1
    if col > 3:
        col = 0
        row += 1

if __name__ == '__main__':
    root.mainloop()