"""キーボードのキーを押下した際の各種処理"""
# utils.pyの関数format_resultをインポート
from utils import format_result

# キーボード操作の設定
def key_input(event, screen, state): 
    key = event.char
    current = screen.get()
    operators = "+-*/%."

    # 数字と演算子
    if key in "0123456789+-*/().":
        # just_evaluatedがTrue→イコールが押されている場合
        if state.just_evaluated and key.isdigit():
            screen.set(key)
        else:
            screen.set(current + key)
        state.just_evaluated = False
        return
    
    # 演算子を押下した際の処理
    if key in operators:
        # 文字列の長さが0の場合→入力できない
        if len(current) == 0:
            return
        # 文字列の末尾に演算子が含まれている場合→末尾の演算子を消して入力
        if current[-1] in operators:
            screen.set(current[:-1] + key) 
        # 文字列に演算子が含まれていない場合→そのまま入力    
        else:
            screen.set(current + key)
        state.just_evaluated = False
        return

    # Enterキー 
    if event.keysym == "Return":
        screen.set(format_result(current))
        state.just_evaluated = True
        return 
    
    # Backspaceキー→右端の数字を1桁消す
    if event.keysym == "BackSpace":
        screen.set(current[:-1])
        state.just_evaluated = False
        return
    
    # c押下時にscreenをブランクに変更
    if key.lower() == "c":
        screen.set("")
        state.just_evaluated = False
        return