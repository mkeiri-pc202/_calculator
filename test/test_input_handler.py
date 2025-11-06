"""input_handler.pyのテストケースコード(pytest用)

    pytestを利用して単体テストを行う
    外部依存を無くすためにTKinterの代わりのモッククラスと
    format_result()の代わりのmonkeypatchを使用
"""
import pytest
from input_handler import handle_input, CalculatorState, reset_evaluated,after_E, after_E_operator



# モック画面オブジェクト
class MockScreen:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, new_value):
        self.value = new_value


@pytest.fixture
# テスト前処理
def setup():
    screen = MockScreen()
    state = CalculatorState()
    return screen, state

def test_button_multiply(setup):
    screen, state = setup
    screen.set("2") 
    handle_input("×", screen, state)
    assert screen.get() == "2*"

def test_button_divide(setup):
    screen, state = setup
    screen.set("2") 
    handle_input("÷", screen, state)
    assert screen.get() == "2/"

def test_allow_len_number(setup):
    screen, state = setup
    screen.set("111111111111111111") 
    handle_input("9", screen, state)
    assert screen.get() == "111111111111111111"

def test_allow_len_operator(setup):
    screen, state = setup
    screen.set("111111111111111111") 
    handle_input("+", screen, state)
    assert screen.get() == "111111111111111111"

def test_allow_len_clear(setup):
    screen, state = setup
    screen.set("111111111111111111") 
    handle_input("C", screen, state)
    assert screen.get() == ""

def test_number_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("1", screen, state)
    assert screen.get() == "1"

def test_continuous_number_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("1", screen, state)
    assert screen.get() == "1"

def test_number_input_decimals(setup):
    screen, state = setup
    screen.set("0.") 
    handle_input("1", screen, state)
    assert screen.get() == "0.1"

def test_number_input_operator(setup):
    screen, state = setup
    screen.set("1+") 
    handle_input("2", screen, state)
    assert screen.get() == "1+2"

def test_number_input_reset(setup, monkeypatch):
    screen, state = setup
    screen.set("1+2")
    monkeypatch.setattr("input_handler.format_result", lambda expr: "3")
    handle_input("=", screen, state)
    handle_input("4", screen, state)
    assert screen.get() == "4"

def test_number_input_zero(setup):
    screen, state = setup
    screen.set("0") 
    handle_input("5", screen, state)
    assert screen.get() == "5"

def test_number_input_zero2(setup):
    screen, state = setup
    screen.set("5+0") 
    handle_input("6", screen, state)
    assert screen.get() == "5+6"

def test_number_input_open_parenthesis(setup):
    screen, state = setup
    screen.set("(") 
    handle_input("7", screen, state)
    assert screen.get() == "(7"

def test_clear_input_number(setup):
    screen, state = setup
    screen.set("90") 
    handle_input("C", screen, state)
    assert screen.get() == ""

def test_clear_input_operator(setup):
    screen, state = setup
    screen.set("√") 
    handle_input("C", screen, state)
    assert screen.get() == ""

def test_clear_input_formula(setup):
    screen, state = setup
    screen.set("(1+2)*√3") 
    handle_input("C", screen, state)
    assert screen.get() == ""

def test_clear_input_reset(setup, monkeypatch):
    screen, state = setup
    screen.set("4+5*6")
    monkeypatch.setattr("input_handler.format_result", lambda expr: "34")
    handle_input("=", screen, state)
    handle_input("C", screen, state)
    assert screen.get() == ""

def test_equal_input(setup, monkeypatch):
    """monkeypatchを利用したイコール入力の検証テスト

    monkeypacthを利用して一時的にformat_result関数をモック化、
    返り値を"3"に固定してhandle_input()の動作だけ検証
    format_result()を呼び出すケース(依存関係)は
    monkeypatchでダミーの関数に置き換え
    
    Args:
        setup (_type_): テスト時の共通設定
        monkeypatch (_type_): その場のプロセスだけプログラムの実行範囲を変える
    """
    screen, state = setup
    screen.set("1+2") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "3")
    handle_input("=", screen, state)
    assert screen.get() == "3"

def test_equal_input_operator(setup, monkeypatch):
    screen, state = setup
    screen.set("3+") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "3+")
    handle_input("=", screen, state)
    assert screen.get() == "3+"

def test_equal_input_parentheses(setup, monkeypatch):
    screen, state = setup
    screen.set("((2+3") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "5")
    handle_input("=", screen, state)
    assert screen.get() == "5"

def test_equal_input_exc(setup, monkeypatch):
    screen, state = setup
    screen.set("abc+5") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "エラー")
    handle_input("=", screen, state)
    assert screen.get() == "エラー"

def test_equal_input_parentheses_formula(setup, monkeypatch):
    screen, state = setup
    screen.set("(5+3)") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "8")
    handle_input("=", screen, state)
    assert screen.get() == "8"

def test_equal_input_parentheses_formula_root_percent(setup, monkeypatch):
    screen, state = setup
    screen.set("(√2+5%)") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "エラー")
    handle_input("=", screen, state)
    assert screen.get() == "エラー"

def test_equal_input_clear(setup, monkeypatch):
    screen, state = setup
    screen.set("C") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "エラー")
    handle_input("=", screen, state)
    assert screen.get() == "エラー"

def test_percent_input_number(setup, monkeypatch):
    screen, state = setup
    screen.set("5") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "0.05")
    handle_input("%", screen, state)
    assert screen.get() == "0.05"

def test_percent_input_exc(setup, monkeypatch):
    screen, state = setup
    screen.set("abc") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "エラー")
    handle_input("%", screen, state)
    assert screen.get() == "エラー"

def test_percent_input_blank(setup, monkeypatch):
    screen, state = setup
    screen.set("") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "")
    handle_input("%", screen, state)
    assert screen.get() == ""

def test_percent_input_operator(setup, monkeypatch):
    screen, state = setup
    screen.set("√") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "")
    handle_input("%", screen, state)
    assert screen.get() == "√"

def test_percent_input_halfway(setup, monkeypatch):
    screen, state = setup
    screen.set("6+7*") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "6+7*")
    handle_input("%", screen, state)
    assert screen.get() == "6+7*"

def test_percent_input_parentheses(setup, monkeypatch):
    screen, state = setup
    screen.set("(8)") 
    monkeypatch.setattr("input_handler.format_result", lambda expr: "(0.08)")
    handle_input("%", screen, state)
    assert screen.get() == "(0.08)"

def test_root_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("√", screen, state)
    assert screen.get() == "√"

def test_root_number_input(setup):
    screen, state = setup
    screen.set("√") 
    handle_input("2", screen, state)
    assert screen.get() == "√2"

def test_root_input_number(setup):
    screen, state = setup
    screen.set("3") 
    handle_input("√", screen, state)
    assert screen.get() == "3√"

def test_root_input_operator(setup):
    screen, state = setup
    screen.set("2*") 
    handle_input("√", screen, state)
    assert screen.get() == "2*√"

def test_root_input_open_parenthesis(setup):
    screen, state = setup
    screen.set("(") 
    handle_input("√", screen, state)
    assert screen.get() == "(√"

def test_double_root_input(setup):
    screen, state = setup
    screen.set("√") 
    handle_input("√", screen, state)
    assert screen.get() == "√√"

def test_triple_root_input(setup):
    screen, state = setup
    screen.set("√√") 
    handle_input("√", screen, state)
    assert screen.get() == "√√"

def test_root_input_halfway(setup):
    screen, state = setup
    screen.set("5+3") 
    handle_input("√", screen, state)
    assert screen.get() == "5+3√"

def test_root_input_exc(setup):
    screen, state = setup
    screen.set("ABC") 
    handle_input("√", screen, state)
    assert screen.get() == "エラー"

def test_puls_minus_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("±", screen, state)
    assert screen.get() == ""

def test_puls_minus_input_minus(setup):
    screen, state = setup
    screen.set("1") 
    handle_input("±", screen, state)
    assert screen.get() == "(-1)"

def test_puls_minus_input_minus_decimals(setup):
    screen, state = setup
    screen.set("0.1") 
    handle_input("±", screen, state)
    assert screen.get() == "(-0.1)"

def test_puls_minus_input_puls(setup):
    screen, state = setup
    screen.set("(-1)") 
    handle_input("±", screen, state)
    assert screen.get() == "1"

def test_puls_minus_input_puls_decimals(setup):
    screen, state = setup
    screen.set("(-0.1)") 
    handle_input("±", screen, state)
    assert screen.get() == "0.1"

def test_puls_minus_input_operator(setup):
    screen, state = setup
    screen.set("2+") 
    handle_input("±", screen, state)
    assert screen.get() == "2+"

def test_puls_minus_input_halfway_minus(setup):
    screen, state = setup
    screen.set("5*3") 
    handle_input("±", screen, state)
    assert screen.get() == "5*(-3)"

def test_puls_minus_input_halfway_puls(setup):
    screen, state = setup
    screen.set("5*(-3)") 
    handle_input("±", screen, state)
    assert screen.get() == "5*3"

def test_puls_minus_input_halfway_decimals_minus(setup):
    screen, state = setup
    screen.set("6/0.5") 
    handle_input("±", screen, state)
    assert screen.get() == "6/(-0.5)"

def test_puls_minus_input_halfway_decimals_plus(setup):
    screen, state = setup
    screen.set("6/(-0.5)") 
    handle_input("±", screen, state)
    assert screen.get() == "6/0.5"

def test_puls_minus_input_parentheses_minus(setup):
    screen, state = setup
    screen.set("(9)") 
    handle_input("±", screen, state)
    assert screen.get() == "((-9))"

def test_puls_minus_input_parentheses_puls(setup):
    screen, state = setup
    screen.set("((-9))") 
    handle_input("±", screen, state)
    assert screen.get() == "(9)"

def test_open_parenthesis_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("(", screen, state)
    assert screen.get() == "("

def test_open_parenthesis_input_number(setup):
    screen, state = setup
    screen.set("1") 
    handle_input("(", screen, state)
    assert screen.get() == "1*("

def test_open_parenthesis_input_operator(setup):
    screen, state = setup
    screen.set("2+") 
    handle_input("(", screen, state)
    assert screen.get() == "2+("

def test_open_parenthesis_puls_minus(setup):
    screen, state = setup
    screen.set("(-3)") 
    handle_input("(", screen, state)
    assert screen.get() == "(-3)*("

def test_open_parenthesis_input_halfway(setup):
    screen, state = setup
    screen.set("12+3*") 
    handle_input("(", screen, state)
    assert screen.get() == "12+3*("

def test_continuous_open_parenthesis_input(setup):
    screen, state = setup
    screen.set("(") 
    handle_input("(", screen, state)
    assert screen.get() == "(("

def test_open_parenthesis_input_open_parenthesis_and_number(setup):
    screen, state = setup
    screen.set("(6") 
    handle_input("(", screen, state)
    assert screen.get() == "(6*("

def test_close_parenthesis_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input(")", screen, state)
    assert screen.get() == ""

def test_close_parenthesis_input_open_parenthesis(setup):
    screen, state = setup
    screen.set("1") 
    handle_input(")", screen, state)
    assert screen.get() == "1"

def test_close_parenthesis_input_number(setup):
    screen, state = setup
    screen.set("1") 
    handle_input(")", screen, state)
    assert screen.get() == "1"

def test_close_parenthesis_input_open_parenthesis_and_number(setup):
    screen, state = setup
    screen.set("(2") 
    handle_input(")", screen, state)
    assert screen.get() == "(2)"

def test_close_parenthesis_input_operator(setup):
    screen, state = setup
    screen.set("√") 
    handle_input(")", screen, state)
    assert screen.get() == "√"

def test_close_parenthesis_input_number_and_operator(setup):
    screen, state = setup
    screen.set("9+") 
    handle_input(")", screen, state)
    assert screen.get() == "9+"

def test_close_parenthesis_input_puls_minus(setup):
    screen, state = setup
    screen.set("(-4)") 
    handle_input(")", screen, state)
    assert screen.get() == "(-4)"

def test_parentheses_more_open(setup):
    screen, state = setup
    screen.set("(2*(5+3") 
    handle_input("=", screen, state)
    assert screen.get() == "16"

def test_parentheses_more_close(setup):
    screen, state = setup
    screen.set("(2*(5+3)))") 
    handle_input("=", screen, state)
    assert screen.get() == "エラー"

def test_E_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("E", screen, state)
    assert screen.get() == ""

def test_E_input_operator(setup):
    screen, state = setup
    screen.set("√") 
    handle_input("E", screen, state)
    assert screen.get() == "√"

def test_E_input_number(setup):
    screen, state = setup
    screen.set("2") 
    handle_input("E", screen, state)
    assert screen.get() == "2E"

def test_puls_input_number_and_E(setup):
    screen, state = setup
    screen.set("2E") 
    handle_input("+", screen, state)
    assert screen.get() == "2E+"

def test_invalid_operator_input_number_and_E(setup):
    screen, state = setup
    screen.set("2E") 
    handle_input("/", screen, state)
    assert screen.get() == "2E"

def test_evaluation_E_without_exponent(setup):
    screen, state = setup
    screen.set("2E") 
    handle_input("=", screen, state)
    assert screen.get() == "2E"

def test_evaluation_number_and_E(setup, monkeypatch):
    screen, state = setup
    screen.set("2E") 
    handle_input("3", screen, state)
    monkeypatch.setattr("input_handler.format_result", lambda expr: "2000")
    handle_input("=", screen, state)
    assert screen.get() == "2000"

def test_plus_minus_with_E_formula(setup):
    screen, state = setup
    screen.set("3E4") 
    handle_input("±", screen, state)
    assert screen.get() == "3E(-4)"

def test_percent_with_E_formula(setup):
    screen, state = setup
    screen.set("3E(-4)") 
    handle_input("±", screen, state)
    assert screen.get() == "3E4"

def test_formula_with_decimal_and_E(setup, monkeypatch):
    screen, state = setup
    screen.set("1.2E3")
    monkeypatch.setattr("input_handler.format_result", lambda expr: "1200")
    handle_input("=", screen, state)
    assert screen.get() == "1200"

def test_formula_with_decimal_exponent(setup, monkeypatch):
    screen, state = setup
    screen.set("2E0.5")
    monkeypatch.setattr("input_handler.format_result", lambda expr: "10")
    handle_input("=", screen, state)
    assert screen.get() == "10"

def test_reinput_E_formula(setup):
    screen, state = setup
    screen.set("3E3")
    handle_input("=", screen, state)
    assert state.just_evaluated is True
    handle_input("E", screen, state)
    assert screen.get() == "3000E"

def test_invalid_expression_with_E(setup):
    screen, state = setup
    screen.set("AbcE+D") 
    handle_input("=", screen, state)
    assert screen.get() == "エラー"

def test_operator_input(setup):
    screen, state = setup
    screen.set("") 
    handle_input("+", screen, state)
    assert screen.get() == ""

def test_operator_input_number(setup):
    screen, state = setup
    screen.set("2") 
    handle_input("+", screen, state)
    assert screen.get() == "2+"

def test_multiple_operators_input_number(setup):
    screen, state = setup
    screen.set("2+") 
    handle_input("*", screen, state)
    assert screen.get() == "2*"

def test_operator_input_open_parenthesis(setup):
    screen, state = setup
    screen.set("(") 
    handle_input("+", screen, state)
    assert screen.get() == "("

def test_operator_input_close_parenthesis(setup):
    screen, state = setup
    screen.set("(2+3)") 
    handle_input("+", screen, state)
    assert screen.get() == "(2+3)+"

def test_operator_input_evaluation(setup):
    screen, state = setup
    screen.set("2+3") 
    handle_input("=", screen, state)
    assert state.just_evaluated is True
    handle_input("/", screen, state)
    assert screen.get() == "5/"

def test_operator_input_invalid_expression(setup):
    screen, state = setup
    screen.set("Abc") 
    handle_input("-", screen, state)
    assert screen.get() == "エラー"

def test_initial_evaluated_flag(setup):
    screen, state = setup
    assert state.just_evaluated is False

def test_reset_evaluated_sets_flag_false(setup):
    screen, state = setup
    state.just_evaluated = True
    reset_evaluated(state)
    assert state.just_evaluated is False

def test_evaluated_flag_true_after_equal_input(setup):
    screen, state = setup
    screen.set("1+2")
    handle_input("=", screen, state)
    assert state.just_evaluated is True

def test_evaluated_flag_true_after_percent_conversion(setup):
    screen, state = setup
    screen.set("2")
    handle_input("%", screen, state)
    assert state.just_evaluated is True

def test_evaluated_flag_false_after_number_input(setup):
    screen, state = setup
    screen.set("")
    state.just_evaluated = True
    handle_input("1", screen, state)
    assert state.just_evaluated is False

def test_evaluated_flag_false_after_sqrt_input(setup):
    screen, state = setup
    screen.set("")
    state.just_evaluated = True
    handle_input("√", screen, state)
    assert state.just_evaluated is False

def test_evaluated_flag_false_after_open_parenthesis(setup):
    screen, state = setup
    screen.set("")
    state.just_evaluated = True
    handle_input("(", screen, state)
    assert state.just_evaluated is False

def test_evaluated_flag_false_after_E_input(setup):
    screen, state = setup
    screen.set("2")
    state.just_evaluated = True
    handle_input("(", screen, state)
    assert state.just_evaluated is False

def test_evaluated_flag_unchanged_after_toggle_sign(setup):
    screen, state = setup
    screen.set("3")
    state.just_evaluated = True
    handle_input("±", screen, state)
    assert state.just_evaluated is True

def test_evaluated_flag_false_after_number_input_post_evaluation(setup):
    screen, state = setup
    screen.set("3+4")
    handle_input("=", screen, state)
    assert state.just_evaluated is True
    handle_input("1", screen, state)
    assert state.just_evaluated is False

def test_evaluated_flag_false_after_operator_input_post_evaluation(setup):
    screen, state = setup
    screen.set("3+4")
    handle_input("=", screen, state)
    assert state.just_evaluated is True
    handle_input("/", screen, state)
    assert state.just_evaluated is False

def test_evaluated_flag_false_after_clear_input_post_evaluation(setup):
    screen, state = setup
    screen.set("3+4")
    handle_input("=", screen, state)
    assert state.just_evaluated is True
    handle_input("C", screen, state)
    assert state.just_evaluated is False

def test_is_last_char_E():
    assert after_E("12E") is True

def test_is_last_char_not_E():
    assert after_E("12E+") is False

def test_is_last_char_E_plus():
    assert after_E_operator("12E+") is True

def test_is_last_char_E_minus():
    assert after_E_operator("12E-") is True

def test_is_last_char_not_E_plus_or_minus():
    assert after_E_operator("12E") is False
