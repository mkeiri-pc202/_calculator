"""数式の評価を行うユーティリティモジュール
    結果の表示が統一されていなかったので、結果を受け取り'全体計算'関数で評価
    結果が整数か小数かで表示を変更する
    また、'ALLOWED_OPERATORS'で入力可能な演算子を設定

import:
    全体計算(from keisan): 与えられた数式を評価し、結果を返す関数   
"""

from keisan import 全体計算

ALLOWED_OPERATORS = "+-*/%.^√E"

def format_result(expr: str) -> str:
    """数式文字列を評価して、結果を文字列として返す
    
    'keisan.py' モジュールの'全体計算'関数を使用して、与えられた数式を評価
    評価結果が整数なら整数で、小数が含まれる場合は浮動小数点数として文字列化
    評価中に例外が発生した場合、"エラー"を返す

    Args:
        expr(str): 計算対象の数式文字列 使用可能な演算子は "+-*/%.^√"
    Returns:
        str: 評価結果の文字列。例外が発生したら"エラー"を返す
    """
    try:
        result = 全体計算(expr)
        # num = float(result)
        if result != '':
            return result
        else:
            return "エラー"
    except Exception:
        return "エラー"
    # try:
    #     result = 全体計算(expr)
    #     num = float(result)
    #     if num.is_integer():
    #         return str(int(num))
    #     else:
    #         return str(num)
    # except Exception:
    #     return "エラー"