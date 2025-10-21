"""電卓のGUIの設定と実行"""

import tkinter as tk
from input_handler import handle_input, CalculatorState

root = tk.Tk()
root.title("電卓")

screen = tk.StringVar()
entry = tk.Entry(root, textvariable=screen, font="Arial 20", justify="right", state="readonly")# ウィジェットを画面のグリッドに配置(最上段、左端、五列分の幅を持たせる)
entry.grid(row=0, column=0, columnspan=5)

state = CalculatorState()

# ラッパー関数の定義(コードの分離や整理、拡張性を持たせるため)して、screenを渡す
def handle_click(event):
    text = event.widget.cget("text") if hasattr(event.widget, "cget") else "="
    handle_input(text, screen, state)

def handle_key(event):
    key = event.char
    if event.keysym == "Return":
        handle_input("=", screen, state)
    elif event.keysym == "BackSpace":
        screen.set(screen.get()[:-1])
        state.just_evaluated = False
    else:
        handle_input(key, screen, state)

def handle_keypress(event, screen, state):
    key = event.char
    if event.keysym == "Return":
        handle_input("=", screen, state)
    elif event.keysym == "BackSpace":
        screen.set(screen.get()[:-1])
        state.just_evaluated = False
    else:
        handle_input(key, screen, state)

entry.bind("<Return>", lambda event: handle_input("=", screen, state))
root.bind("<Key>", lambda event: handle_keypress(event, screen, state))

# ボタンの設定
buttons = [
    "√", "±", " ", " ",
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