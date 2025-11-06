"""数式の評価を行うユーティリティモジュール
    結果を受け取り'全体計算'関数で評価
    結果が''(空文字)であれば"エラー"を表示、それ以外は結果を表示
    また、'ALLOWED_CHARS'で入力可能な文字を設定
    'ALLOWED_OPERATORS'で入力可能な演算子を設定

import:
    全体計算(from keisan): 与えられた数式を評価し、結果を返す関数   
"""

from keisan import 全体計算

ALLOWED_CHARS = "0123456789+-*/().%^√±E=C"
ALLOWED_OPERATORS = "+-*/%^√E."

def format_result(expr: str) -> str:
    """数式文字列を評価して、結果を文字列として返す
    
    'keisan.py' モジュールの'全体計算'関数を使用して、与えられた数式を評価
    評価結果が''(空文字)や例外が発生した場合は"エラー"を表示、それ以外は結果を返す。

    Args:
        expr(str): 計算対象の数式文字列
    Returns:
        str: 評価結果の文字列。空文字列または例外が発生したら"エラー"を返す
    """
    try:
        result = 全体計算(expr)
        if result != '':
            return result
        else:
            return "エラー"
    except Exception:
        return "エラー"