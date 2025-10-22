from utils import format_result
from utils import ALLOWED_OPERATORS
import re


class CalculatorState:
    def __init__(self):
        self.just_evaluated = False


def handle_input(text: str, screen, state):
    current = screen.get()

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
        if len(current) == 0 or current[-1] in ALLOWED_OPERATORS + "(":
            return
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
    
    # 演算子(べき乗とプラスマイナスキーの処理も)
    if text in ALLOWED_OPERATORS or text == "*" or text == "-":
        if len(current) == 0:
            return
        if current[-2:] == "**":
            return
        if current[-2:] == "--":
            return
        if current[-1] == "*" and text == "*":
            screen.set(current + text)
            return
        if current[-1] == "-" and text == "-":
            screen.set(current + text)
            return
        if current[-1] in ALLOWED_OPERATORS:
            screen.set(current[:-1] + text)
        else:
            screen.set(current + text)
        return
    
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
        if current.count("(") > current.count(")"):
            if current[-1] in "(":
                return
            else:
                screen.set(current + text)
        else:
            return
        state.just_evaluated = False
        return

    # 計算後の数字の追記を防ぐ処理
    if state.just_evaluated:
        if text in ALLOWED_OPERATORS:
            screen.set(current + text)
        else:
            screen.set(text)
    else:
        screen.set(current + text)
    state.just_evaluated = False
    return
