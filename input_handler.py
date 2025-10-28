"""電卓の入力処理を行うモジュール
CalculatorStateクラスで計算の実行状況をフラグで表示
handle_input関数で電卓の入力に応じて処理、画面に表示
数字以外の特殊入力(クリア、イコール、パーセント、ルート、括弧、プラスマイナス、指数表記)にも対応

import:
    format_result(from utils): 計算結果を整形して表示用に変換
    ALLOWED_OPERATORS(from utils): 入力を許可している演算子のリスト
    re(標準ライブラリ): パーセントの正規表現マッチングに使用
"""

from utils import format_result
from utils import ALLOWED_OPERATORS
import re


class CalculatorState:
    """計算の状態を保持するクラス

    Attributes:
        just_evaluated (bool): 直前に計算が実行されたか(イコールを実行)示すフラグ
    """
    def __init__(self):
        """CalculatorStateの初期化

        self.just_evaluatedをFalseに設定
        """
        self.just_evaluated = False


def handle_input(text: str, screen, state):
    """電卓の入力を処理し、画面に反映

    入力に応じて数式を構築・評価、結果を画面に表示する。
    特殊な入力(クリア、イコール、パーセント、ルート、括弧、プラスマイナス、指数表記)にも対応

    Args:
        text (str): 入力された文字
        screen (tk.StringVar): Tkinterの表示用変数。数式や結果を表示
        state (CalculatorState): 電卓の状態管理オブジェクト。直前の計算実行状態を保持
    """

    current = screen.get()
    miss_parenthesis = current.count("(") - current.count(")")

    # ボタン表記を内部記号に変換
    if text == "×":
        text = "*"
    elif text == "÷":
        text = "/"

    # 19文字以上だったらクリア以外入力できない
    if len(current) >=19 and text not in ("c","C"):
        return

    # クリア
    if text.lower() == "c":
        screen.set("")
        state.just_evaluated = False
        return
    
    # イコール
    if text == "=":
        if current and current[-1] in ALLOWED_OPERATORS:
            return
        else:
            try:
                if miss_parenthesis > 0:
                    current += miss_parenthesis * ")"
                result = format_result(current)
                screen.set(result)
            except Exception as e:
                screen.set("エラー")
                print(e)
        state.just_evaluated = True
        return
            
    # パーセント
    if text == "%":
        try:
            match = re.search(r'(\d+(\.\d+)?)%?$', current)
            if match:
                value = float(match.group(1)) / 100
                new_expr = re.sub(r'(\d+(\.\d+)?)%?$', str(value), current)
                screen.set(new_expr)
                state.just_evaluated = True
            else:
                screen.set("エラー")
        except Exception as e:
            screen.set("エラー")
            print(e)
        state.just_evaluated = True
        return
    
    # ルート
    if text == "√":
        if state.just_evaluated or current == "0":
            screen.set(text)
        elif len(current) >= 2 and current[-2:] == "√√":
            return
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return

    
    # プラスマイナス
    if text == "±":
        # 入力した文字がなし、もしくは最後の文字列が演算子 + ( の場合は入力できない
        if len(current) == 0 or current[-1] in ALLOWED_OPERATORS + "(":
            return
        # 文字列の最後が")"かつ文字列を右から検索して"("が右端になく、かつ文字列を右端から検索して"("の左隣に"-"がある場合(=負数)
        if current[-1] == ")" and current.rfind("(") != -1 and current[current.rfind("(") + 1] == '-':
            # rfind("(")で最後の"()"を検索、数値を抽出して反転
            last_parentheses_index = current.rfind("(")
            target = current[last_parentheses_index:]
            cleaned = target.replace("(", "").replace(")", "")
            result = str(int(cleaned) * -1)
            screen.set(current[:last_parentheses_index] + result)
            return
        # 正数の場合
        else:
            last_op_index = max((current.rfind(op) for op in ALLOWED_OPERATORS))
            target = current if last_op_index == -1 else current[last_op_index + 1:]
            new_text = f"(-{target})"
            screen.set(current[:last_op_index + 1] + new_text)
        return

    # 括弧
    if text == "(":
        if len(current) == 0:
            screen.set(text)
        elif current[-1] in "1234567890E":
            screen.set(current + "*" + text)
        else:    
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    if text == ")":
        if miss_parenthesis != 0 and current[-1] != "(":
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    # # 指数(E)
    if text == "E":
        if len(current) == 0:
            return
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    # 指数表記後の演算子入力(加算か減算のみ入力可)
    if current and current[-1] == "E":
        if text in "*/%.^E": 
            return
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return
    if  len(current) >= 2 and current[-2] == "E" and current[-1] in "+-":
        if text in "+-":
            screen.set(current[:-1] + text)
        elif text in "+-*/%.^E":
            return
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    # 数字
    if text.isdigit():
        if state.just_evaluated:
            screen.set(text)
        else:
            if current == "0" or (len(current) >= 2 and current[-1] == "0" and current[-2] in "+-/*"):
                screen.set(current[:-1] + text)
            elif current and current[-1] in ")":
                screen.set(current + "*" + text)
            else:
                screen.set(current + text)
        state.just_evaluated = False
        return     
    
    # 演算子
    if text in "+-*/%.^":
        if len(current) == 0:
            return
        if current[-1] in "+-*/%.^":
            screen.set(current[:-1] + text)
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return
