# from sympy import sympify
# import re

# def cal(data:str):
#     """
#     概要
#     数式文字列dataを受け取り、その中身をcheckdataでチェックしてから、
#     sympifyを使って、計算を行い計算結果を返す。
#     計算エラーが出た場合は、エラー表示を行い、Falseを返す。
#     dataが数式表現として、不適当な場合はFalseを返す。

#     詳細
#         pip install sympy 1.14
    
#         変数
#             仮引数  data   : 文字列 数式を表現したもの
#             戻り値  result : 数値 計算が正常に行われた場合の計算結果
#                              bool(False) 計算ができない場合
#     """

#     if checkdata(data):
#         try:
#             result = sympify(data)
#         except Exception as ex:
#             print('計算できません', ex)
#             result = False
#     else:
#         # print('データの()が閉じられていない')
#         result = False

#     return result

# def checkdata(data:str)-> bool:
#     """
#     概要
#     数式の文字列dataが数式として成り立つ文字列か調べる。
    
#     詳細
#         チェック内容
#           ( と ) の数が等しいか
#           数字と演算子 0-9 . ( ) + - * / 以外の文字はないか（空白はNG)

#         仮引数 data : 文字列 数式
#         戻り値 bool : 問題がある場合のみ、Falseとする
          
#         その他の変数
#          leftc : ( の数。
#          rightc : ) の数。
#     """

#     leftc=data.count('(')
#     rightc=data.count(')')

#     # print(data,leftc, rightc)

#     if leftc != rightc:
#         print('データの()が閉じられていない')
#         return False
    
#     data = data.replace('**','^')
#     if bool(re.search(r'[+\-*/]{2,}', data)):
#         print(f'{data}演算子が２個以上続いています')
#         return False
    
#     data = data.replace('^','**')
    
#     return bool(re.fullmatch(r'[0-9.()+\-*/ ]+', data))
#     # return bool(re.fullmatch(r'[1-9\.\+\(\)\-\*/]+', data))


# def 小数以下ゼロ前の桁数(num):
#     """
#     概要
#         プリント表示で浮動小数の小数点以下に000...と並ぶのを防ぐために
#         小数点以下で0以外の数がある桁数を調べる

#     変数
#         引数 num: 数値 調べる数
#         戻り数 j: 小数点以下で0以外の数がある桁数

#         文字num : 引数numの文字表示
#         length  : 文字numの文字数
#         i       : 0の数のカウント 右側から1,2...と数える
#         ゼロの数 : トータルの0の数
#         j       : 0 以外の数のカウント i に続けてカウントする

#     """



#     if abs(num - int(num)) < 1e-10:
#         return 0
    
#     文字num = str(num)
#     length = len(文字num)
#     i = 0
#     while True:
#         # print(文字num[length-i-1:length-i])
#         if 文字num[length-i-1:length-i] !='0':
#             break
#         else:
#             i = i + 1
#     ゼロの数=  i
#     j = ゼロの数
#     while True:
#         if 文字num[length-j-1:length-j] =='.':
#             return j - i
#         j = j + 1
#         if j == length:
#             return 0
            

# if __name__=='__main__':

#     testdata = [
#         '1+2',
#         '2*3',
#         '1.1+2*3',
#         '(1+2)*(3+4)',
#         '2**2',
#         '-2**-2',
#         '--2+3',
#         '2-(-(3-1))',
#         '.25+.25',
#         '1/*2',
#         '2**3',
#         '2***3'
#     ]
#     for data in testdata:
#         result = cal(data)
#         j = 小数以下ゼロ前の桁数(result)
#         # print(j)
#         print(f'{data} = {result:.{j}f}')