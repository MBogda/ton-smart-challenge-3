import unittest
from typing import Any, Union


def eval_solution(text: str) -> int:
    return eval(text.replace("/", "//"))


def parse_number(text: str) -> tuple[str, int]:
    idx = 0
    while text[idx].isspace():
        idx += 1

    negative = False
    if text[idx] == '-':
        negative = True
    while text[idx].isspace():
        idx += 1

    number = 0
    while text[idx].isdigit():
        number = number * 10 + int(text[idx])
        idx += 1
        if idx == len(text):
            break
    return text[idx:], -number if negative else number


def parse_operator(text: str) -> tuple[str, str]:
    idx = 0
    while text[idx].isspace():
        idx += 1
        if idx == len(text):
            break
    operator = text[idx]
    idx += 1
    return text[idx:], operator


def if_parenthesis(text: str, open_: bool) -> tuple[str, bool]:
    idx = 0
    while text[idx].isspace():
        idx += 1
    if open_ and text[idx] == '(':
        return text[idx + 1:], True
    if not open_ and text[idx] == ')':
        return text[idx + 1:], True
    return text[idx:], False


def parse_expression(text: str) -> tuple[str, list]:
    text, parenthesis = if_parenthesis(text, open_=True)
    if parenthesis:
        text, left = parse_expression(text)
        # text, parenthesis = if_parenthesis(text, open_=False)
        # if not parenthesis:
        #     raise ValueError()
    else:
        text, left = parse_number(text)
    root: list[Union[int, str, list]] = [left, None, None]
    node = root
    while text:
        text, parenthesis = if_parenthesis(text, open_=False)
        if parenthesis:
            return text, root
        text, operator = parse_operator(text)
        text, number = parse_number(text)
        if operator in ("*", "/"):
            node[0] = [node[0], operator, number]
        elif operator in ("+", "-"):
            node[1] = operator
            node[2] = [number, None, None]
            node = node[2]
        else:
            raise ValueError
    return "", root


def compute_expression(node: list) -> int:
    if isinstance(node[0], list):
        left = compute_expression(node[0])
    else:
        left = node[0]
    if isinstance(node[2], list):
        right = compute_expression(node[2])
    else:
        right = node[2]

    if node[1] == "+":
        return left + right
    elif node[1] == "-":
        return left - right
    elif node[1] == "*":
        return left * right
    elif node[1] == "/":
        return left // right
    elif node[1] is None:
        return left


def tree_solution(text: str) -> int:
    _, node = parse_expression(text)
    return compute_expression(node)


def text_calculator(text: str) -> int:
    # return eval_solution(text)
    return tree_solution(text)


class Test(unittest.TestCase):
    def test_simple_operations(self):
        input_text = "2 + 3"
        expected = 5
        self.assertEqual(text_calculator(input_text), expected)

    def test_simple_operations2(self):
        input_text = "2 - 3"
        expected = -1
        self.assertEqual(text_calculator(input_text), expected)

    def test_simple_operations3(self):
        input_text = "2 * 3"
        expected = 6
        self.assertEqual(text_calculator(input_text), expected)

    def test_simple_operations4(self):
        input_text = "2 / 3"
        expected = 0
        self.assertEqual(text_calculator(input_text), expected)

    def test_simple_operations5(self):
        input_text = "(2 + 3)"
        expected = 5
        self.assertEqual(text_calculator(input_text), expected)

    def test_corner_cases(self):
        input_text = "2 + -3"
        expected = -1
        self.assertEqual(text_calculator(input_text), expected)

    def test_corner_cases2(self):
        input_text = "2"
        expected = 2
        self.assertEqual(text_calculator(input_text), expected)

    def test_corner_cases3(self):
        input_text = "-2"
        expected = -2
        self.assertEqual(text_calculator(input_text), expected)

    def test_corner_cases4(self):
        input_text = "3 / 3"
        expected = 1
        self.assertEqual(text_calculator(input_text), expected)

    def test_corner_cases5(self):
        input_text = "4 / 3"
        expected = 1
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations(self):
        input_text = "2 + 2 * 2"
        expected = 6
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations1(self):
        input_text = "(2 + 2) * 2"
        expected = 8
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations2(self):
        input_text = "2 + 2 / 4 - 2"
        expected = 0
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations3(self):
        input_text = "(2 + 2) / (4 - 2)"
        expected = 2
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations4(self):
        input_text = "(2 + 2) / 4 - 2"
        expected = -1
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations5(self):
        input_text = "(10000 - 84) * (456 / 450 + 22) + 7 / (34 + 12) + 8 / 34 + 9"
        expected = 228077
        self.assertEqual(text_calculator(input_text), expected)
