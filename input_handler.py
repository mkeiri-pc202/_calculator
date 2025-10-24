from utils import format_result
from utils import ALLOWED_OPERATORS
import re


class CalculatorState:
    """電卓の状態を保持するクラス

    Attributes:

    """
    def __init__(self):
        self.just_evaluated = False


def handle_input(text: str, screen, state):
    current = screen.get()

    # ボタン表記を内部記号に変換
    if text == "×":
        text = "*"
    elif text == "÷":
        text = "/"
    # elif text == "^":
    #     text = "**"

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
        if current[-1] in ALLOWED_OPERATORS:
            return
        else:
            try:
                result = format_result(current)
                screen.set(result)
                state.just_evaluated = True
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
        return
    
    # プラスマイナス
    if text == "±":
        # 入力した文字がなし、もしくは最後の文字列が演算子 + ( の場合は入力できない
        if len(current) == 0 or current[-1] in ALLOWED_OPERATORS + "(":
            return
        # 文字列の最後が)かつ文字列を右から検索して(が右端になく、かつ文字列を右端から検索して
        if current[-1] == ")" and current.rfind("(") != -1 and current[current.rfind("(") + 1] == '-':
            last_parentheses_index = current.rfind("(")
            target = current[last_parentheses_index:]
            cleaned = target.replace("(", "").replace(")", "")
            result = str(int(cleaned) * -1)
            screen.set(current[:last_parentheses_index] + result)
            return
        last_op_index = max((current.rfind(op) for op in ALLOWED_OPERATORS))
        target = current if last_op_index == -1 else current[last_op_index + 1:]
        new_text = f"(-{target})"
        screen.set(current[:last_op_index + 1] + new_text)
        return

    # # プラスマイナス(正規表現で判定)
    # if text == "±":
    #     if len(current) == 0 or current[-1] in ALLOWED_OPERATORS + "(":
    #         return
        
    #     # 通常時のマイナス付け替え
    #     match = re.match(r'^-?\d+(\.\d+)?$', current)
    #     if match:
    #         num = current
    #         if current.startswith("-"):
    #             new_num = num[1:]
    #         else:
    #             new_num = "-" + num
    #         screen.set(new_num)
    #         state.just_evaluated = False
    #         return
        
    #     # 演算子直後の数字のマイナス付け替え
    #     match = re.search(r'([+\-*/(])(-?\d+(\.\d+)?)(?!.*[+\-*/(])', current)
    #     if match:
    #         num_start = match.start(2)
    #         num = match.group(2)

    #         if num.startswith("-"):
    #             new_num = num[1:]
    #         else:
    #             new_num = "-" + num

    #         new_expr = current[:num_start] + new_num + current[num_start + len(num):]
    #         screen.set(new_expr)
    #         state.just_evaluated = False
    #         return

    #     # ()内の数字のマイナス付け替え
    #     match = re.search(r'\((\-?\d+(\.\d+)?)\)(?!.*\()', current)
    #     if match:
    #         full = match.group(0)
    #         num = match.group(1)

    #         if num.startswith("-"):
    #             new = "(" + num[1:] + ")"
    #         else:
    #             new = "(-" + num + ")"

    #         new_expr = current[:match.start()] + new + current[match.end():]
    #         screen.set(new_expr)
    #         state.just_evaluated = False
    #         return

    # 括弧
    if text == "(":
        if len(current) == 0:
            screen.set(text)
        elif current[-1] in "1234567890":
            screen.set(current + "*" + text)
        else:    
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    if text == ")":
        if current.count("(") > current.count(")") and current[-1] != "(":
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    # 数字
    if text.isdigit():
        if state.just_evaluated:
            screen.set(text)
            state.just_evaluated = False
        else:
            if current == "0" or (len(current) >= 2 and current[-1] == "0" and current[-2] in "+-/*"):
                screen.set(current[:-1] + text)
            elif current and current[-1] in ")":
                screen.set(current + "*" + text)
            else:
                screen.set(current + text)
        state.just_evaluated = False
        return
    
    # 演算子(べき乗の処理も)
    if text in ALLOWED_OPERATORS:
        if len(current) == 0:
            return
        if current[-2:] == "**":
            return
        if current[-1] == "*" and text == "*":
            screen.set(current + text)
            return
        if current[-1] in ALLOWED_OPERATORS:
            screen.set(current[:-1] + text)
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return

    # # 計算後の数字の追記を防ぐ処理
    # if state.just_evaluated:
    #     if text in ALLOWED_OPERATORS:
    #         screen.set(current + text)
    #     else:
    #         screen.set(text)
    #     state.just_evaluated = False
    # else:
    #     screen.set(current + text)
    #     return
