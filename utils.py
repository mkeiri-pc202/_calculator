""" 結果が整数か小数か判断して、表示形式を変える関数
- 結果の表示が統一されていなかったので、結果が整数の場合はint、小数の場合はfloatにして文字列に返す
"""

from sympy import sympify

def format_result(expr: str) -> str:
    """数式を評価して、整数なら整数、小数なら小数として文字列で返す関数

    :param expr: 入力した数式
    :type expr: str
    :return: 評価結果を文字列で返す。例)5の場合は整数、2.5は小数、評価に失敗した場合はエラー
    :rtype: str
    """
    # sympify関数を利用して入力した式(expr)を取り込み、resultに代入
    result = sympify(expr)
    # 成功
    try:
        # 結果を浮動小数点型にしてnumに代入
        num = float(result)
        # is_integer()メソッドで整数か小数か判定
        if num.is_integer():
            # True(整数)の場合は整数型にして文字列で返す
            return str(int(num))
        else:
            # False(小数)の場合はそのまま浮動小数点型で文字列で返す
            return str(num)
    # 例外はエラーで返す
    except Exception:
        return "エラー"