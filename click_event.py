"""ウィンドウのボタンを押下した際の各種処理"""

# tkとしてtkinterをインポート
import tkinter as tk
# utils.pyの関数format_resultをインポート
from utils import format_result


"""'='(イコール)を押下したかフラグで管理するモジュール
- 計算結果後に数字を入れると計算結果の末尾に数字が入ってしまうエラーの対策
- 計算結果直後かどうかを判定するためにフラグを保持するクラス
- 複数ファイル間で使用するためにファイルを作成
- 初期値はFalse
"""
class CalculatorState:
    """電卓の状態を保持するクラス
    :Attributes just_evaluated (bool): 直前にイコール(計算)が実行されたかどうかを示すフラグ
    """
    def __init__(self):
        self.just_evaluated = False

# click関数(ウィンドウのボタンの処理設定)
def click(event, screen, state):
    """_summary_

    :param event: _description_
    :type event: _type_
    :param screen: _description_
    :type screen: _type_
    :param state: _description_
    :type state: _type_
    """
    #イベントが発生したウィジェットをwidget変数に代入
    widget = event.widget
    # クリックされたのがボタンかどうか判断
    if isinstance(widget, tk.Button):
        # 押下したボタンのテキストを取得
        text = event.widget.cget("text")
    # ボタン以外(キーボードのEnter等)を押下した場合でも計算は実行
    else:
        text = '='

    # 19文字以上だったらクリア以外入力できない
    if len(screen.get()) >=19 and text not in ("c","C"):
        return

    # イコールを押下した際の動作
    if text == "=":
        # 成功
        try:
            result = format_result(screen.get())
            # resultをスクリーンに表示
            screen.set(result)
            # just_evaluatedをTrueに変える
            state.just_evaluated = True
        # 例外が発生した場合
        except Exception as e:
            # スクリーンに'エラー'を表示
            screen.set("エラー")
            # just_evaluatedをTrueに変える
            state.just_evaluated = True
    # C(クリア)を押下した場合        
    elif text == "C":
        # ''をスクリーンに表示→クリア
        screen.set("")
        # just_evaluatedをFalseに変える
        state.just_evaluated = False
    # 上記以外(イコール、クリア以外のボタンを押した場合)
    
    elif text == "±":
        current = screen.get()
        print(current)
        
        if len(current) == 0 or current[-1] in  ['+', '-', '*', '/','%','(']:
            return
        
        if current[-1] == ')' and current.rfind('(') != -1 and current[current.rfind('(') +1] == '-':
        
            last_parentheses_index = max((current.rfind(op) for op in ['(']))       
            target = current if last_parentheses_index == 0 else current[last_parentheses_index:]
            # target = current[current.rfind('-'):]
            cleaned_target = target.replace('(', '').replace(')', '')
            result = float(cleaned_target) * -1
            screen.set(current[:last_parentheses_index] + str(result))
            return
        
        last_op_index = max((current.rfind(op) for op in ['+', '-', '*', '/','%']))       
        target = current if last_op_index == -1 else current[last_op_index + 1:]
        
        if last_op_index == -1:
            new_text = "(-" + target + ")"
            screen.set(new_text)
            
        else:
            new_text = "(-" + target + ")"
            screen.set(current[:last_op_index + 1] + new_text)

    
    elif text == "%":
        current = screen.get()
        
        if len(current) == 0 or current[-1] in  ['+', '-', '*', '/','%','(',')']:
            return
        
        last_op_index = max((current.rfind(op) for op in ['+', '-', '*', '/','%']))  
        if last_op_index == -1:
            screen.set(str(int(current.rstrip('%')) / 100))
            return
        screen.set(current[:last_op_index + 1] + str(int(current[last_op_index + 1].rstrip('%')) / 100))
    
    elif text in "+-*/.":
        current = screen.get()
        if len(current) == 0:
            return       
        if current and current[-1] in "+-*/%.":
            screen.set(current[:-1] + text)     
        else:
            screen.set(current + text)
        state.just_evaluated = False
        
    elif text in "0":
        current = screen.get()
        if current == "0" or (len(current) >= 2 and current[-1] == "0" and  current[-2] in "+-/*"):
            return
        else:
            screen.set(current + text)
        state.just_evaluated = False 

    elif text in "123456789":
        current = screen.get()
        if current == "0" or len(current) >= 2 and current[-1] =="0" and current[-2] in "+-/*":
            screen.set(current[:-1] + text)
        else:
            screen.set(current + text)
        state.just_evaluated = False    
    
    
    else:
        # just_evaluatedがTrueの場合
        if state.just_evaluated:
            # 演算子の場合
            if text in "+-*/":
                # 結果を使って続けて計算
                screen.set(screen.get() + text)
            # 数字の場合
            else:
                # 新しい式として開始
                screen.set(text)
        # just_evaluatedがFalseの場合
        else:
            # 結果を使って続けて計算
            screen.set(screen.get() + text)
        # just_evaluatedをFalseに変える
        state.just_evaluated = False
