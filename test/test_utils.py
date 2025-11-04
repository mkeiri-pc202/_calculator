"""utils.pyの単体テスト用テストコード

monkeypatchを使用して全体計算()をモック化
format_result()を呼び出してもモックの返り値が返るようにして
期待する出力が得られるかを確認
"""

import pytest
from utils import format_result


def test_format_result(monkeypatch):
    def mock_全体計算(expr):
        return "24.0"
    monkeypatch.setattr("utils.全体計算", mock_全体計算)
    assert format_result("3*8") == "24"

def test_format_result_float(monkeypatch):
    def mock_全体計算(expr):
        return "1.25"
    monkeypatch.setattr("utils.全体計算", mock_全体計算)
    assert format_result("5/4") == "1.25"

def test_format_result_error_on_invalid(monkeypatch):
    def mock_全体計算(expr):
        return "Abc"
    monkeypatch.setattr("utils.全体計算", mock_全体計算)
    assert format_result("Abc") == "エラー"

def test_format_exception(monkeypatch):
    def mock_全体計算(expr):
        raise ValueError("エラー")
    monkeypatch.setattr("utils.全体計算", mock_全体計算)
    assert format_result("1/0") == "エラー"