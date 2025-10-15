"""電卓のGUIの設定と実行"""

# tkとしてtkinterをインポート
import tkinter as tk
# click関数を使うために同フォルダのclick_event.pyとkey_inputをインポート
import click_event
import key_input
from click_event import CalculatorState

# tk(tkinterをインポート)をroot(ウインドウ)に代入
root = tk.Tk()
# タイトル設定
root.title("電卓")

# Widget変数としてStringVarを利用、screen変数とする
screen = tk.StringVar()
# Entryウィジェットでscreenと連携で入力内容を管理。フォントと文字寄せを指定
entry = tk.Entry(root, textvariable=screen, font="Arial 20", justify="right", state="readonly")# ウィジェットを画面のグリッドに配置(最上段、左端、五列分の幅を持たせる)
entry.grid(row=0, column=0, columnspan=5)

state = CalculatorState()

# ラッパー関数の定義(コードの分離や整理、拡張性を持たせるため)して、screenを渡す
def handle_click(event):
    click_event.click(event, screen, state)
def handle_key(event):
    key_input.key_input(event, screen, state)

# キーボードを押下したら、handle_click関数を呼び出す(=キーボード操作対応)
entry.bind("<Return>", handle_click)
# ウィンドウのボタンを押下したら、handle_key関数を呼び出す
root.bind("<Key>", handle_key)

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
# ボタンの位置を始める位置を設定(1行目、左端)
row, col = 1, 0
# ボタンのループ処理(buttonsリストの文字列に対して繰り返し処理)
for button in buttons:
    # ボタンを作成(ボタンに表示する文字,フォントとサイズ, ボタンの幅, 高さ)
    btn = tk.Button(root, text=button, font="Arial 15", width=5, height=2)
    # ボタンをグリッドに配置(row=行, col=列)
    btn.grid(row=row, column=col)
    # ボタンがマウスの左クリックされたとき、click関数を呼び出す
    btn.bind("<Button-1>", handle_click)
    # ボタンをひとつずつ配置し、その度列番号を1つ進める
    col += 1
    # 4列目まで配置したら次の行に移動して列をリセット
    if col > 3:
        col = 0
        row += 1

if __name__ == '__main__':
    # ウインドウ表示実行ループ
    root.mainloop()