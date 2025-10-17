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

#キー入力と実行する機能との紐づけ
def handle_key(event):
    match event.char:
        case '0':
            button_widget = root.nametowidget('.!button21')
            event.widget = button_widget  # ウィジェットオブジェクトをセット
        case '1':
            button_widget = root.nametowidget('.!button17')
            event.widget = button_widget  # ウィジェットオブジェクトをセット
        case '2':
            button_widget = root.nametowidget('.!button18')
            event.widget = button_widget  # ウィジェットオブジェクトをセット
        case '3':
            button_widget = root.nametowidget('.!button19')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '4':
            button_widget = root.nametowidget('.!button13')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '5':
            button_widget = root.nametowidget('.!button14')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '6':
            button_widget = root.nametowidget('.!button15')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '7':
            button_widget = root.nametowidget('.!button9')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '8':
            button_widget = root.nametowidget('.!button10')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '9':
            button_widget = root.nametowidget('.!button11')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '%':
            button_widget = root.nametowidget('.!button7')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case 'c'|'C':
            button_widget = root.nametowidget('.!button8')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '(':
            button_widget = root.nametowidget('.!button5')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case ')':
            button_widget = root.nametowidget('.!button6')
            event.widget = button_widget  # ウィジェットオブジェクトをセット  
        case '.':
            button_widget = root.nametowidget('.!button22')
            event.widget = button_widget  # ウィジェットオブジェクトをセット  
        case '='|'\r':
            button_widget = root.nametowidget('.!button23')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '+':
            button_widget = root.nametowidget('.!button24')
            event.widget = button_widget  # ウィジェットオブジェクトをセット    
        case '-':
            button_widget = root.nametowidget('.!button20')
            event.widget = button_widget  # ウィジェットオブジェクトをセット 
        case '*':
            button_widget = root.nametowidget('.!button16')
            event.widget = button_widget  # ウィジェットオブジェクトをセット 
        case '/':
            button_widget = root.nametowidget('.!button12')
            event.widget = button_widget  # ウィジェットオブジェクトをセット
        case '\x08':
            button_widget = root.nametowidget('.!button4')
            event.widget = button_widget  # ウィジェットオブジェクトをセット   
        case _:
            return #上記にないキーを押下したときにエラーになってたので追記
        
    click_event.click(event, screen, state)
        
# キーボードを押下したら、handle_click関数を呼び出す(=キーボード操作対応)
entry.bind("<Return>", handle_click)
# ウィンドウのボタンを押下したら、handle_key関数を呼び出す
root.bind("<Key>", handle_key)

# ボタンの設定
buttons = [
    "√", "±", " ", "BS",
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

button_refs = {}
for button in buttons:
    # ボタンを作成(ボタンに表示する文字,フォントとサイズ, ボタンの幅, 高さ)
    btn = tk.Button(root, text=button, font="Arial 15", width=5, height=2, state="normal")
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