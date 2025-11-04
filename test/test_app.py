"""app.pyのテストケースコード(pytest用)

    pytestを利用して単体テストを行う
    外部依存を無くすためにunittest.mockモジュールと
    monkeypatchを使用
"""
import pytest
from unittest.mock import Mock
import tkinter as tk
from app import handle_click, handle_key
from input_handler import CalculatorState


@pytest.fixture
def setup_tk():
    root = tk.Tk()
    screen = tk.StringVar()
    state = CalculatorState()
    return root, screen, state

def test_handle_click_number(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)
    monkeypatch.setattr("app.screen", screen)
    monkeypatch.setattr("app.state", state)

    btn = tk.Button(root, text="7")
    event = Mock()
    event.widget = btn

    handle_click(event)
    mock_handle_input.assert_called_once_with("7", screen, state)

def test_handle_click_operator(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)
    monkeypatch.setattr("app.screen", screen)
    monkeypatch.setattr("app.state", state)

    btn = tk.Button(root, text="+")
    event = Mock()
    event.widget = btn

    handle_click(event)
    mock_handle_input.assert_called_once_with("+", screen, state)

def test_handle_key_return(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = ""
    event.keysym = "Return"

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("=", screen, state)

def test_handle_key_backspace_number(setup_tk):
    root, screen, state = setup_tk
    screen.set("123")
    event = Mock()
    event.char = ""
    event.keysym = "BackSpace"

    handle_key(event, screen, state)
    assert screen.get() == "12"
    assert state.just_evaluated is False

def test_handle_key_backspace_operator(setup_tk):
    root, screen, state = setup_tk
    screen.set("1+")
    event = Mock()
    event.char = ""
    event.keysym = "BackSpace"

    handle_key(event, screen, state)
    assert screen.get() == "1+"

def test_handle_key_backspace_evaluated(setup_tk):
    root, screen, state = setup_tk
    screen.set("123")
    event = Mock()
    event.char = ""
    event.keysym = "BackSpace"

    handle_key(event, screen, state)
    assert state.just_evaluated is False

def test_handle_key_allowed_char(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "+"
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("+", screen, state)

def test_handle_key_disallowed_char(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "a"
    event.keysym = ""

    result = handle_key(event, screen, state)
    mock_handle_input.assert_not_called()
    assert result is None

def test_handle_key_open_parentheses(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "("
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("(", screen, state)

def test_handle_key_close_parentheses(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = ")"
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with(")", screen, state)

def test_handle_key_decimal_point(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "√"
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("√", screen, state)

def test_handle_key_hat(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "^"
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("^", screen, state)

def test_handle_key_plus_minus(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "±"
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("±", screen, state)

def test_handle_key_E(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = "E"
    event.keysym = ""

    handle_key(event, screen, state)
    mock_handle_input.assert_called_once_with("E", screen, state)

def test_handle_key_blank(monkeypatch, setup_tk):
    root, screen, state = setup_tk
    mock_handle_input = Mock()
    monkeypatch.setattr("app.handle_input", mock_handle_input)

    event = Mock()
    event.char = ""
    event.keysym = ""

    result = handle_key(event, screen, state)
    mock_handle_input.assert_not_called()
    assert result is None