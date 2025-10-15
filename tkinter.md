
# 呼び出し
import tkinter as tk
import tkinter.ttk as ttk #

# rootメインウィンドウの設定
root = tk.Tk() # インスタンス作成
root.title("Frame") # タイトル作成　
root.geometry("300x100") #Windowの幅の調整

# Frameを設定する
frame = tk.Frame(root,[options])
frame.pack() #Frameを設置する
frame_left.pack_propagate(False) #うまく動かなければ追加

# Frame（フレーム）のオプション引数
width	int	フレームの横幅
height	int	フレームの縦幅
relief	flat（デフォルト）,raised
sunken,groove,ridge	フレームの枠を指定
bg or background	color	フレームの背景色
bd or borderwidth	int	ボーダーの幅
cursor	マウスポインタの種類	マウスポインタの見た目を指定
pady	int	枠とテキストとの間の縦の空白
padx	int	枠とテキストとの間の横の空白
takefocus	True, False	Tabキーでのフォーカス移動の有無


# .pack()のオプションを設定する
side(位置をざっくり決める)

label2 = tk.Label(root, text="上")
label2.pack(side="top") #上に積み上げる

label2 = tk.Label(root, text="下")
label2.pack(side="bottom")

label2 = tk.Label(root, text="下")
label2.pack(side="bottom")

label2.pack(fill="x") #横幅いっぱいにする（widthは無視
label2.pack(fill="y") #縦幅いっぱいにする（heightは無視


# grid(表を作成する)
grid(row = 0, column = 0,)

row	整数	ウィジェットを配置するセルの行番号
column	整数	ウィジェットを配置するセルの列番号
rowspan	整数	ウィジェットがまたがるセルの行数
columnspan	整数	ウィジェットがまたがるセルの列数
ipadx	整数	ウィジェット内側のx方向の余白
ipady	整数	ウィジェット内側のy方向の余白
padx	整数
タプル	ウィジェット外側のx方向の余白
pady	整数
タプル	ウィジェット外側のy方向の余白
sticky	文字列	ウィジェットのセル内での配置場所
in_	ウィジェット	親ウィジェット(コンテナ)を指定

# Label
label_1 = tk.Label(frame,text=1,width=2,height=1)

# Button
button_1 = tk.Button(frame,text=1,width=2,height=1)

# Text
text_1 = tk.Entry(frame,width=20)

# exeにする
pyinstaller app.py --onedir --onefile --noconsole

# 仮想環境を出力する
conda activate [your_env_name]
conda env export --from-history > environment.yml

# 仮想環境をインポートする
conda env create -f environment.yml