from sympy import sympify, Float, sqrt, N
import re

def cal(data:str):
    """
    概要
    数式文字列dataを受け取り、その中身をcheckdataでチェックしてから、
    sympifyを使って、計算を行い計算結果を返す。
    計算エラーが出た場合は、エラー表示を行い、Falseを返す。
    dataが数式表現として、不適当な場合はFalseを返す。

    詳細
        pip install sympy 1.14
    
        変数
            仮引数  data   : 文字列 数式を表現したもの
            戻り値  result : 数値 計算が正常に行われた場合の計算結果
                             'エラー' 計算ができない場合
                    文字result :小数点を含めた桁数 n にした文字列数字
    """
    
    #平方根√があるか調べ、あれば、
    # 　√(/文字数字 | 文字式)　   または　　　　　　 √文字数字を
    # 　sqrt(文字数字 | 文字式) 注()内は変えない　　sqrt(文字数字) 
    # に置き換える

    if '√' in data:
        data = 平方根文字をsqrtに変換(data)
        # print('24行目', data)
        # result = sympify(data)
        # result = sympify(str(1+math.sqrt(33)-math.sqrt(22)*math.sqrt(22)))
        # print('26行目', float(result))

    #まだ√が残っているか確認する
    if '√' in data:
        print('29行目 √がまだあります')

    #文字 data 内に数字0-9、小数点.、指数e、演算子(+,-,*,/,**,√)以外の字があるか
    # ()が閉じられているか調べ、OKなら、sympifyを使った計算を行いresultに返す

    if checkdata(data):
        if 'e(' in data:
            data = 指数のカッコ削除(data)
        try:
            print('33行目 data', data)

            result = sympify(data)

            print('25行目',result, Float(N(result),18))

            # 文字result = str(result)
            # sqrt()を計算するために、N関数を使う
            result = Float(N(result))
            文字result = str(result)
            print('41行目 result 文字result', result, 文字result)

            # (　無効 : 桁数19以上だとエラーになる)
            #計算結果resultから、n桁以下にした文字数字とを作る
            #桁数 n の設定

# 指数 e がある場合の処理

            if 'e' in 文字result:
                文字result一時置き場 = 文字result
                仮数ptn = re.compile(r'([.0-9+-]*)e')
                仮数obj = 仮数ptn.search(文字result)

                指数ptn = re.compile(r'e(\(?[0-9.+\-*/]*\)?)')
                指数obj = 指数ptn.search(文字result)
                print('67指数入り')
                if 仮数obj:
                    仮数 = 仮数obj.group(1)
                    print('64 文字result前 文字result後', 文字result一時置き場,仮数)

                仮数整形後 = 文字成形ゼロ削除(仮数)
                if 仮数整形後 and 仮数:
                    文字result = 文字result一時置き場.replace(仮数, str(仮数整形後))
                    print('69 仮数整形後 文字result',仮数整形後, 文字result)
            
                if 指数obj:
                    指数 = 指数obj.group(1)
                    print('79 指数',指数)
                    指数の改善表示 = 指数.lstrip('(')
                    指数の改善表示 = 指数.rstrip(')')
                    文字result = 文字result.replace(指数の改善表示,指数) 
                    print('指数改善後',文字result)
                return result,文字result
            
            # print('72文字result',文字result)
            文字result整形後 = 文字成形(文字result)
            # print('74文字result',文字result整形後)
            return result, 文字result整形後

        except Exception as ex:
            # print('計算できません', ex)
            result = 'エラー','エラー'

    else:
        # print('データの()が閉じられていない')
        result = 'エラー','エラー'

    return result

def 指数のカッコ削除(data):
    """
    eの後にある( )の中を計算し、()を外す

    """
    data一時置き場 = data
    指数ptn = re.compile(r'e(\([0-9.+\-*/]*\))')
    指数obj = 指数ptn.search(data)
    # print('67指数入り')
    
    if 指数obj:
        指数前 = 指数obj.group(1)
        print('116 指数',指数前)
        指数部の計算後= str(sympify(指数前))
        print('指数計算後',指数部の計算後)
        print('119 data', data)
        data = data.replace(指数前,指数部の計算後)
        # data = data.replace('(2)', '2')
        print ('120 指数部の変更後のdata', data)
    return data

def 文字成形ゼロ削除(num_str):
    """
    指数表示で小数点以下で、末尾まで続く 0 を削除する
    num_str 仮数部分
    """
    文字長さ = len(num_str)
    i = 0
    print('87 num_str')
    for i in range(0, 文字長さ):
        if num_str[-1] == '0':
            num_str = num_str[:-1]
            i = i + 1
        else:
            return num_str
            




def 文字成形(文字result):
            #計算結果 result の桁数計算
            計算結果桁数 = len(文字result)
            # print('計算結果桁数',文字result,計算結果桁数)

            #文字resultの表記を改善する
            #小数点以下で0が続く場合、0を取り除く
            #小数点以下がない場合、小数点を表示しない
            if 計算結果桁数 > 1:

                文字result = 小数点以下を整える(文字result)
                # result = Float(result, 16)
                # print('57行目', 文字result)

                n = 16
                スライス後文字result= 文字result[:n]
                # print(f'59行目 {n}桁にする{スライス後文字result}')
                # print('119 スライス後文字result',スライス後文字result)
            return スライス後文字result
            # return result
            

            #     #指数表示か調べる
            #     eE_有無ptn = re.compile(r'[eE]')
                
            #     if eE_有無ptn.search(文字result):
            #         print('指数表示で桁数オーバーです エラーにします')
            #         仮数ptn = re.compile(r'(^[-+0-9.]+)')
            #         仮数元 = 仮数ptn.search(文字result)
            #         print('仮数', 仮数元)
            #         if 仮数元:
            #             仮数部=仮数元.group(0)
            #             print('変更前仮数部',仮数部)
            #             仮数部長さ = len(仮数部)
            #             削除回数 = 仮数部長さ- 16

            #             for i in range(0,削除回数):
            #                 仮数部 = 仮数部[:-1]
            #                 print('変更仮数部',仮数部)
                    
            #     # result = result


def 平方根文字をsqrtに変換(num_str):
    """
    from sympfy import sqrt が必要。sqrt()を使うから。
    
    作業
    文字式列num_strの中にある √ を sympy.sqrtに書き換える
    その後、
    1. sqrt(数字)の場合は、そのまんま返す
    2. sqrt+数字 つまり()がない場合は、sqrt(数字) の形にする
    
    変数
        仮引数 num_str √を含む文字式
    戻り変数
        num_str sqrt(数字/数式)の形で返す

    変数    
        ルートptn    'sqrt'+'数字0-9と. e'が複数続くパターン : √()でなく、√数字 だけの場合
        検索結果全体 ルートptnで調べたsqrtに続く数字があるか、の検索結果全体
        検索結果     あった場合、上記検索結果の個々の要素
    """
   
    # print('num_str', num_str)
   # √を sqrt に替える。
    num_str = num_str.replace('√', 'sqrt')

    #√数字のパターンを作る sqrtの後に、()がなく、数字、指数e、小数点.が続く場合
    ルートptn = re.compile(r'sqrt([0-9.e]+)')

    #正規表現の適合を調べる 適合結果は、検索結果　として取り出す
    検索結果全体 = ルートptn.findall(num_str)
    for 検索結果 in 検索結果全体:
        # print('検索結果',検索結果)

        # 検索結果は文字数字なので、置き換えは、sqrt文字数字　を　sqrt(文字数字)にする
        num_str=num_str.replace('sqrt'+検索結果,'sqrt('+検索結果+')')
        # print('変換結果',num_str)

    #変換したsqrt(文字数字)をnum_strとして返す
    return num_str


def checkdata(data:str)-> bool:
    """
    概要
    数式の文字列dataが数式として成り立つ文字列か調べる。
    
    詳細
        チェック内容
          ( と ) の数が等しいか
          数字と演算子 0-9 . ( ) + - * e/ sqrt 以外の文字はないか（空白はNG)

        仮引数 data : 文字列 数式
        戻り値 bool : 問題がある場合のみ、Falseとする
          
        その他の変数
         leftc : ( の数。
         rightc : ) の数。
    """

    leftc=data.count('(')
    rightc=data.count(')')

    # print(data,leftc, rightc)

    if leftc != rightc:
        print('データの()が閉じられていない')
        return False
    
    data = data.replace('**','^')
    if bool(re.search(r'[+\-*/]{2,}', data)):
        print(f'{data}演算子が２個以上続いています')
        return False
    
    data = data.replace('^','**')

    #文字の検査　数字、演算子、sqrt 以外ではないこと

    # boolA = bool(re.fullmatch(r'[0-9.()+\-*/]+', data))
    boolA = bool(re.fullmatch(r'[0-9.e()+\-*/\(sqrt\)]+', data))
    print('boolA', boolA)
    
    return boolA
    # return bool(re.fullmatch(r'[1-9\.\+\(\)\-\*/]+', data))

def 小数点以下を整える(num):

    ゼロの数, 小数点以下のゼロでない数 = 小数点以下ゼロの桁数(num)
    # print('169 ゼロの数, 小数点以下のゼロでない数の数', ゼロの数, 小数点以下のゼロでない数)

       
    ゼロの位置 = len(num)-ゼロの数

    if 小数点以下のゼロでない数 == 0:
        ゼロの位置 = ゼロの位置 -1

    ゼロを取り除いた文字数字 = num[:ゼロの位置]

    # print('172 ゼロを取り除いた文字数字', ゼロを取り除いた文字数字)
    
    return ゼロを取り除いた文字数字


def 小数点以下ゼロの桁数(num):
    """
    概要
        プリント表示で浮動小数の小数点以下に000...と並ぶのを防ぐために
        小数点以下で0以外の数がある桁数を調べる

    変数
        引数 num: 数値 調べる数
        戻り数 j: 小数点以下で0以外の数がある桁数

        文字num : 引数numの文字表示
        length  : 文字numの文字数
        i       : 0の数のカウント 右側から1,2...と数える
        ゼロの数 : トータルの0の数
        j       : 0 以外の数のカウント i に続けてカウントする

    """

    
    # if abs(num - int(num)) < 1e-10:
    #     return 0
    
    文字num = str(num)
    文字num長さ = len(文字num)

    if '.' not in num:
        return 0, 0
    
    i = 0
    while i <= 文字num長さ:
        # print(文字num[length-i-1:length-i])
        if 文字num[文字num長さ-i-1:文字num長さ-i] !='0':
            break
        else:
            i = i + 1
    ゼロの数=  i
    # print(('文字num長さ,ゼロの数'),文字num長さ, ゼロの数)
    
    j = 0
    
    while j <= 文字num長さ - ゼロの数:
        if 文字num[文字num長さ-ゼロの数-j-1:文字num長さ-ゼロの数-j] =='.':
            小数点以下のゼロでない数 = j
            break
        else:
            j = j + 1
            # print('222行目、j', j)
        # if j == length:

        #     return ゼロの数, j
    # print('216ゼロの数, 小数点以下のゼロでない数の数', ゼロの数, 小数点以下のゼロでない数)    
    return ゼロの数, 小数点以下のゼロでない数
        
            
        

if __name__=='__main__':

    
    testdata = [
        '1e(2+3*3)'
        # '√1e10',
        # '1.1+2*3',
        # '(1+2)*(3+4)',
        # '2**2',
        # '-2**-2',
        # '--2+3',
        # '2-(-(3-1))',
        # '.25+.25',
        # '1/*2',
        # '2**3',
        # '2***3'
    ]
    for data in testdata:
        result, 文字result整形後 = cal(data)
        # print('320result, 文字result整形後',result, 文字result整形後)
        print(f'{data} = {result}, {文字result整形後}')
        print()


        # j = 小数以下ゼロ前の桁数(result)
        # print(j)
        # if j == 0:
        #     print(f'{data} = {result}')
        # else:
        #     print(f'{data} = {result:.{j}f}')
        
if __name__ == '__main__':
    print(f'result{cal('1+2')}')