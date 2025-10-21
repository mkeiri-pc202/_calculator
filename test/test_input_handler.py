import pytest
from input_handler import handle_input, CalculatorState
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# モック画面オブジェクト
class MockScreen:
    def __init__(self):
        self.value = ""

    def get(self):
        return self.value

    def set(self, new_value):
        self.value = new_value

@pytest.fixture
def setup():
    screen = MockScreen()
    state = CalculatorState()
    return screen, state

def test_digit_input(setup):
    screen, state = setup
    handle_input("1", screen, state)
    assert screen.get() == "1"

def test_operator_input(setup):
    screen, state = setup
    screen.set("1")
    handle_input("+", screen, state)
    assert screen.get() == "1+"

def test_evaluation(setup):
    screen, state = setup
    screen.set("2+3")
    handle_input("=", screen, state)
    assert screen.get() == "5"

def test_clear(setup):
    screen, state = setup
    screen.set("123")
    handle_input("C", screen, state)
    assert screen.get() == ""

def test_percent(setup):
    screen, state = setup
    screen.set("50")
    handle_input("%", screen, state)
    assert screen.get() == "0.5"

def test_chain_after_evaluation(setup):
    screen, state = setup
    screen.set("2+3")
    handle_input("=", screen, state)
    handle_input("+", screen, state)
    handle_input("4", screen, state)
    assert screen.get() == "5+4"
