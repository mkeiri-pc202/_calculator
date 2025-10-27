"""結果を評価して、文字列で返す関数
    結果の表示が統一されていなかったので、結果を受け取り'全体計算'関数で評価
    keisan.pyから全体計算のインポートが必要

    また、'ALLOWED_OPERATORS'で入力可能な演算子を設定
"""

# from sympy import sympify
from keisan import 全体計算

ALLOWED_OPERATORS = "+-*/%.^√"

def format_result(expr: str) -> str:
    """keisan.py の全体計算関数を使って数式を評価する
    
    'keisan.py' モジュールの'全体計算'関数を使用して、与えられた数式を評価
    評価中に例外が発生した場合、"エラー"を返す

    Args:
        expr(str): 計算対象の数式文字列 使用可能な演算子は "+-*/%.^√"
    Returns:
        str: 評価結果の文字列。例外が発生したら"エラー"を返す
    """
    try:
        result = 全体計算(expr)
        return str(result)
    except Exception:
        return "エラー"



# sympify利用の関数
# def format_result(expr: str) -> str:
#     """数式を評価して、整数なら整数、小数なら小数として文字列で返す関数

#     :param expr: 入力した数式
#     :type expr: str
#     :return: 評価結果を文字列で返す。例)5の場合は整数、2.5は小数、評価に失敗した場合はエラー
#     :rtype: str
#     """
    # result = sympify(expr)
    # try:
    #     num = float(result)
    #     if num.is_integer():
    #         return str(int(num))
    #     else:
    #         return str(num)
    # except Exception as e:
    #     return "エラー"