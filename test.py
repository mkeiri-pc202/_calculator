import tkinter as tk

def on_button_click(value):
    print(f"ボタン {value} が押されました")

def on_key_press(event):
    key = event.char
    if key in button_refs:
        button_refs[key].invoke()  # ← ここでボタンを擬似的に「クリック」させる！

root = tk.Tk()
root.title("電卓風キーボード連動")

button_refs = {}  # キー（'1', '2', ...）とボタンを紐づける辞書

# 数字ボタンを作る
for i in range(10):
    key = str(i)
    btn = tk.Button(root, text=key, width=5, height=2, command=lambda k=key: on_button_click(k))
    btn.grid(row=i//5, column=i%5)
    button_refs[key] = btn  # キーとボタンを対応付け

# キー入力をバインド
root.bind("<Key>", on_key_press)

root.mainloop()