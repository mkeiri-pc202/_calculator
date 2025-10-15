"""キーボードのキーを押下した際の各種処理"""

# utils.pyの関数format_resultをインポート
from utils import format_result

# キーボード操作の設定
def key_input(event, screen, state):
    key = event.char
    # 数字と演算子
    if key in "0123456789+-*/":
        # just_evaluatedがTrue→イコールが押されている場合
        if state.just_evaluated:
            #演算子が押下されたら、計算を継続
            if key in "+-*/":
                screen.set(screen.get() + key)
            # 数字が押下されたら、押下した数字を表示
            else:
                screen.set(key)
        # False→計算を継続
        else:
            screen.set(screen.get() + key)
        # just_evaluatedをFalseに変える
        state.just_evaluated = False
    # Enterキー
    elif key == "\r":
        # 成功→計算結果を表示
        try:
            result = format_result(screen.get())
            screen.set(result)
        # 例外はエラー表示
        except Exception as e:
            screen.set("エラー")
        # just_evaluatedをTrueに変える
        state.just_evaluated = True
    # Backspaceキー→右端の数字を1桁消す
    elif key == "\x08":
        screen.set(screen.get()[:-1])
        # just_evaluatedをFalseに変える
        state.just_evaluated = False
    
    # c押下時にscreenをブランクに変更
    elif key in ("c","C"):
        screen.set("")
    state.just_evaluated = False