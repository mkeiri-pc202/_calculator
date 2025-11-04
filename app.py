"""電卓のGUIの設定と実行をするモジュール

TKinterを使用して電卓のインターフェースを作成、
ボタンやキーボード入力に応じて数式を処理。
tkinterのインポート、functoolsモジュールのpartial関数
input_handler`モジュールの handle_input関数とCalculatorStateクラスを利用

import:
    tkinter(標準ライブラリ): 電卓のインターフェースを作成するGUIライブラリ
    functools.partial(標準ライブラリ): 関数の一部の引数を固定した新たな関数を作成する
    handle_input(from input_handler): 入力に応じて数式を構築・評価する関数
    CalulatorState(from input_handler): 計算の状態(イコールしたかどうか)を保持するクラス
"""

import tkinter as tk
from utils import ALLOWED_OPERATORS
from input_handler import handle_input, CalculatorState
from functools import partial

root = tk.Tk()
root.title("電卓")

screen = tk.StringVar()
entry = tk.Entry(root, textvariable=screen, font=("Arial", 20), justify="right", state="readonly", takefocus=0)
entry.grid(row=0, column=0, columnspan=5)

state = CalculatorState()

def handle_click(event):
    """(画面上の)ボタンをクリックされたときに入力を処理する

    イベントオブジェクトからボタンのテキストを取得、
    handle_input関数を呼び出し、入力を処理

    Args:
        event (tkinter.Event): ボタンのクリックイベント
    """
    text = event.widget.cget("text") 
    handle_input(text, screen, state)

def handle_key(event, screen, state):
    """キーボード入力を処理

    入力されたキーが許可された文字(allowed_chars)であれば、handle_input関数を呼び出し処理
    Enterキーで計算実行(イコール)
    Backspaceキーでscreenの末尾が数字の場合、一文字削除してstate.just_evaluatedをFalseにする
    screenの末尾が演算子の場合はreturn
    それ以外のキーはNoneを返す

    Args:
        event (tkinter.Event): キーボードイベント(入力)
        screen (tkinter.StringVar): 表示用の文字列変数
        state (CalculatorState): 電卓の状態管理オブジェクト
    """
    key = event.char
    allowed_chars = "0123456789+-*/().%^√±E"
    
    if event.keysym == "Return":
        handle_input("=", screen, state)
    elif event.keysym == "BackSpace":
        if screen.get()[-1] in ALLOWED_OPERATORS:
            return
        else:
            screen.set(screen.get()[:-1])
            state.just_evaluated = False
    elif key and key in allowed_chars:
        handle_input(key, screen, state)
    else:
        return

# partialでhandle_key関数に引数(screen, state)を固定
bound_handle_key = partial(handle_key, screen=screen, state=state)

# bindメソッドでキー操作によってbound_handle_keyを呼び出す
root.bind("<Key>", bound_handle_key)

# ボタンの設定
buttons = [
    "√", "±", "^", "E",
    "(", ")", "%", "C",
    "7", "8", "9", "÷",
    "4", "5", "6", "×",
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