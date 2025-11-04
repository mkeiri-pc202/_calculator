# 電卓プログラム テスト仕様書

バージョン: 1.1 
最終更新日: [2025/11/04]
作成日: [2025/10/24] 
作成者: [作成者名 / 松本経理ビジネス専門学校 Team A ]  
リポジトリ: [mkeiri-pc202/_calculator](https://github.com/mkeiri-pc202/_calculator)

---

## 1.概要
- 対応プログラム: 電卓(_calculator)
- 対象機能: 四則演算、入力検証、エラーハンドリング
- テスト目的: 各機能が仕様通りに動作することを確認する

## 2.テスト環境
- OS: Windows 11 Education(24H2)
- Python: 3.13.9
- エディタ: Visual Studio Code 1.105.1
- テストフレームワーク: pytest
- 実行方法: ターミナルにて `pytest tests/` を実行
- 依存ライブラリ:
- バージョン管理: Github
- 実行端末: CPU: AMD Athlon Silver 3050U with Radeon Graphics(2.30 GHz) RAM: 8.0GB

## 3.テスト項目一覧
### 3.1 単体テスト一覧
- 対象ファイル:app.py テストファイル:test_app.py
![alt text](image-1.png)

- 対象ファイル:input_handler.py テストファイル:test_input_handler.py
![alt text](image-2.png)

- 対象ファイル:計算.py 

- 対象ファイル:utils.py テストファイル:test_utils.py
![alt text](image-3.png)

### 3.2 統合テスト一覧

### 3.3 総合テスト一覧