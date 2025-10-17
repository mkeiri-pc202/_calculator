"""ウィンドウのボタンを押下した際の各種処理"""

# tkとしてtkinterをインポート
import tkinter as tk
# utils.pyの関数format_resultをインポート
from utils import format_result

"""'='(イコール)を押下したかフラグで管理するモジュール
- 計算結果後に数字を入れると計算結果の末尾に数字が入ってしまうエラーの対策
- 計算結果直後かどうかを判定するためにフラグを保持するクラス
- 複数ファイル間で使用するためにclick_event.pyを作成
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
    #イベントが発生したウィジェットをwidget変数に代入
    widget = event.widget
    # 現在表示してある文字列(screen)をcurrentに代入
    current = screen.get()
    # クリックされたのがボタンかどうか判断
    if isinstance(widget, tk.Button):
        # 押下したボタンのテキストを取得
        text = event.widget.cget("text")
    # ボタン以外(キーボードのEnter等)を押下した場合でも計算は実行
    else:
        text = '='

    # 19文字以上だったらクリア以外入力できない
    if len(current) >=19 and text not in ("c","C"):
        return

    # イコールを押下した際の動作
    if text == "=":
        # 成功
        try:
            result = format_result(current)
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
        return
    
    # BS（バックスペース）を押下した場合
    if text == "BS":
        screen.set(current[:-1])
        state.just_evaluated = False
        return

    # C(クリア)を押下した場合        
    if text == "C":
        # ''をスクリーンに表示→クリア
        screen.set("")
        state.just_evaluated = False
        return
    
    # ±の処理
    if text == "±":
        current = screen.get()
        print(current)

    #数値以外の文字列が入力されていたら処理を飛ばす 
        if len(current) == 0 or current[-1] in  ['+', '-', '*', '/','%','(']:
            return
        
    #負の整数(-1)などが入ってた時に1に戻す処理
        if current[-1] == ')' and current.rfind('(') != -1 and current[current.rfind('(') +1] == '-':
        
            last_parentheses_index = max((current.rfind(op) for op in ['(']))       
            target = current if last_parentheses_index == 0 else current[last_parentheses_index:]
            # target = current[current.rfind('-'):]
            cleaned_target = target.replace('(', '').replace(')', '')
            
            # 変換後の値がすべてfloatになっていたので修正（intに変換した値と別だったらfloatのまま出力
            result = float(cleaned_target) * -1
            if result == int(result):
                result = int(result)            
            screen.set(current[:last_parentheses_index] + str(result))
            return
        
    #正の値(1など)が入ってた時に(-1)に変更する処理
        last_op_index = max((current.rfind(op) for op in ['+', '-', '*', '/','%']))       
        target = current if last_op_index == -1 else current[last_op_index + 1:]
        
        if last_op_index == -1:
            new_text = "(-" + target + ")"
            screen.set(new_text)
            
        else:
            new_text = "(-" + target + ")"
            screen.set(current[:last_op_index + 1] + new_text) 
        return
    
    # %を押下した際の処理
    if text == "%":
        # currentの文字列の長さが0もしくは末尾(-1)に演算子が入っている場合→入力できない
        # √が入らないように追加
        if len(current) == 0 or current[-1] in  ['√','+', '-', '*', '/','%','(',')']:
            return
        try:
            # currentの中で直前にでた演算子の位置を探す
            last_op_index = max((current.rfind(op) for op in ['+', '-', '*', '/','%']))
            # 演算子がない(数字のみ)場合
            if last_op_index == -1:
                # 100で割ってスクリーンに表示 %は削除
                screen.set(str(float(current.rstrip('%')) / 100))
            else:
                # 演算子がある場合は直前の演算子より前はそのまま、直前の演算子の後ろの数字を100で割り、表示
                screen.set(current[:last_op_index + 1] + str(float(current[last_op_index + 1:].rstrip('%')) / 100))
        except Exception as e:
            screen.set("エラー")
            # ログ確認のため
            print(e)
        state.just_evaluated = True
        return  
    
    # 演算子を押下した際の処理
    if text in "+-*/.":
        # 文字列の長さが0の場合→入力できない
        if len(current) == 0:
            return
        # 文字列と文字列の末尾に演算子が含まれている場合
        if current and current[-1] in "√+-*/%.":
            screen.set(current[:-1] + text) 
        # 文字列に演算子が含まれていない場合    
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return

    # 数字を押下した際の処理(isdigitメソッドで文字列が数字であることを判別する)
    if text.isdigit():
        # もう一度呼び出さないとうまくいかなかったので呼び出し
        # current = screen.get()
        if state.just_evaluated:
            # イコールを押下直後(計算直後)なら新しい式として開始
            screen.set(text)
        else:
            # 通常の数字入力処理
            if current == "0" or (len(current) >= 2 and current[-1] == "0" and current[-2] in "+-/*"):
                screen.set(current[:-1] + text)
            else:
                screen.set(current + text)
        state.just_evaluated = False
        return  
    
    # =(イコール)や%(パーセント)を押下直後、数字が追記されてしまうエラーを回避する処理
    # just_evaluatedがTrueの場合
    if state.just_evaluated:
        # 演算子の場合
        if text in "+-*/":
            screen.set(current + text)
        # 数字の場合
        else:
            screen.set(text)
    # just_evaluatedがFalseの場合
    else:
        screen.set(current + text)
    state.just_evaluated = False
