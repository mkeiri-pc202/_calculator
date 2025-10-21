from utils import format_result

class CalculatorState:
    def __init__(self):
        self.just_evaluated = False

def handle_input(text: str, screen, state):
    current = screen.get()
    operators = "+-*/%."

    # クリア
    if text.lower() == "c":
        screen.set("")
        state.just_evaluated = False
        return
    
    # イコール
    if text == "=":
        try:
            result = format_result(current)
            screen.set(result)
        except Exception:
            screen.set("エラー")
        state.just_evaluated = True
        return
    
    # パーセント
    if text == "%":
        if len(current) == 0 or current[-1] in operators + "()":
            return
        try:
            last_op_index = max((current.rfind(op) for op in operators))
            if last_op_index == -1:
                screen.set(str(float(current.rfind("%")) / 100))
            else:
                screen.set(current[:last_op_index + 1] + str(float(current[last_op_index + 1:].rstrip('%')) / 100))
        except Exception:
            screen.set("エラー")
        state.just_evaluated = True
        return
    
    # プラスマイナス
    if text == "±":
        if len(current) == 0 or current[-1] in operators + "(":
            return
        if current[-1] == ")" and current.rfind("(") != -1 and current[current.rfind("(") + 1] == '-':
            last_parentheses_index = current.rfind("(")
            target = current[last_parentheses_index:]
            cleaned = target.replace("(", "").replace(")", "")
            result = str(int(cleaned) * -1)
            screen.set(current[:last_parentheses_index] + result)
            return
        last_op_index = max((current.rfind(op) for op in operators))
        target = current if last_op_index == -1 else current[last_op_index + 1:]
        new_text = f"(-{target})"
        screen.set(current[:last_op_index + 1] + new_text)
        return
        
    
    # 数字
    if text.isdigit():
        if state.just_evaluated:
            if current and current[-1] in "+-*/%.":
                screen.set(text)
            else:
                screen.set(text)
        else:        
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    # 演算子
    if text in operators:
        if len(current) == 0:
            return
        if current[-1] in operators:
            screen.set(current[:-1] + text)
        else:
            screen.set(current + text)
        state.just_evaluated = False
        return
    
    # 括弧
    if text in "()":
        screen.set(current + text)
        state.just_evaluated = False
        return
    
    # その他
    if state.just_evaluated:
        if text in operators:
            screen.set(current + text)
        else:
            screen.set(text)
    else:
        screen.set(current + text)
    state.just_evaluated = False
    return
