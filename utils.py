""" 結果が整数か小数か判断して、表示形式を変える関数
- 結果の表示が統一されていなかったので、結果が整数の場合はint、小数の場合はfloatにして文字列に返す
"""

from sympy import sympify

ALLOWED_OPERATORS = "+-*/%." + "**"

def format_result(expr: str) -> str:
    """数式を評価して、整数なら整数、小数なら小数として文字列で返す関数

    :param expr: 入力した数式
    :type expr: str
    :return: 評価結果を文字列で返す。例)5の場合は整数、2.5は小数、評価に失敗した場合はエラー
    :rtype: str
    """
    result = sympify(expr)
    try:
        num = float(result)
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)
    except Exception as e:
        return "エラー"