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

def reset_evaluated(state: CalculatorState):
    """計算の状態をリセット
    
    関数化して新たに入力が始まる場面にはreset_evaluated(state)を配置
    必要箇所にはstate.just_evaluated = Trueを配置

    Args:
        state (CalculatorState): 計算状況を保持するオブジェクト。計算直後のフラグをリセットする
    """
    state.just_evaluated = False

def after_E(text: str) -> bool:
    """指数表記(E)の入力判定

    文字列の最後の文字がEであるかを判断する

    Args:
        text (str): 判定対象の文字列

    Returns:
        bool: 最後の文字がEであればTrue、それ以外はFalse
    """
    return text.endswith("E")

def after_E_operator(text: str) -> bool:
    """文字列がEに続き、'+'か'-'で終わっているか判定

    Args:
        text (str): 判定対象の文字列

    Returns:
        bool: 最後の文字列がE+かE-であればTrue、それ以外はFalse
    """
    return len(text) >= 2 and text[-2] == "E" and text[-1] in "+-" 

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
        reset_evaluated(state)
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
                return
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
        reset_evaluated(state)
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
            result = str(float(cleaned) * -1)
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
        reset_evaluated(state)
        return
    
    if text == ")":
        if miss_parenthesis != 0 and current[-1] != "(":
            screen.set(current + text)
        return

    # 指数表記(E)
    if text == "E":
        if current and current[-1].isdigit():
            screen.set(current + text)
        reset_evaluated(state)
        return

    # 指数(E)の後、数字か"+","-"のみ入力可
    if after_E(current):
        if text in "+-" or text.isdigit():
            screen.set(current + text)
        return
    
    # E+もしくはE-の後、数字の追加入力か"+","-"の置き換え入力可("+","-"以外の演算子の入力不可)
    if after_E_operator(current):
        if text.isdigit():
            screen.set(current + text)
        elif text in "+-":
            screen.set(current[:-1] + text)
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
        reset_evaluated(state)
        return     
    
    # 演算子
    if text in "+-*/%.^":
        if len(current) == 0:
            return
        if current[-1] in "+-*/%.^":
            screen.set(current[:-1] + text)
        else:
            screen.set(current + text)
        reset_evaluated(state)
        return
