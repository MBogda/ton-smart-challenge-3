import unittest
from typing import Any, Union


def eval_solution(text: str) -> int:
    return eval(text.replace("/", "//"))


def skip_spaces(text: str) -> str:
    idx = 0
    while idx < len(text) and text[idx].isspace():
        idx += 1
    return text[idx:]


def parse_number(text: str) -> tuple[str, int]:
    negative = False
    if text[0] == '-':
        negative = True
        text = skip_spaces(text[1:])

    number = 0
    idx = 0
    while idx < len(text) and text[idx].isdigit():
        number = number * 10 + int(text[idx])
        idx += 1

    return skip_spaces(text[idx:]), -number if negative else number


def parse_operator(text: str) -> tuple[str, str]:
    operator = text[0]
    return skip_spaces(text[1:]), operator


def if_parenthesis(text: str, open_: bool) -> tuple[str, bool]:
    text = skip_spaces(text)
    if open_ and text[0] == '(':
        return skip_spaces(text[1:]), True
    if not open_ and text[0] == ')':
        return skip_spaces(text[1:]), True
    return text, False


def parse_expression(text: str) -> tuple[str, list]:
    text = skip_spaces(text)
    text, parenthesis = if_parenthesis(text, open_=True)
    if parenthesis:
        text, expression = parse_expression(text)
    else:
        text, expression = parse_number(text)
    root: list[Union[int, str, list]] = [expression, None, None]
    node = root
    while text:
        text, parenthesis = if_parenthesis(text, open_=False)
        if parenthesis:
            return text, root
        text, operator = parse_operator(text)

        text, parenthesis = if_parenthesis(text, open_=True)
        if parenthesis:
            text, expression = parse_expression(text)
        else:
            text, expression = parse_number(text)

        if operator in ("*", "/"):
            node[0] = [node[0], operator, expression]
        elif operator in ("+", "-"):
            node[1] = operator
            node[2] = [expression, None, None]
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


def parse_number_stack(text: str, idx: int) -> tuple[int, int]:
    number = 0
    while idx < len(text) and text[idx].isdigit():
        number = number * 10 + int(text[idx])
        idx += 1

    return idx - 1, number


def parse_expression_postfix(text: str) -> list:
    output = []
    operators_stack = []
    idx = 0
    unary = True
    while idx < len(text):
        symbol = text[idx]
        if symbol == ' ':
            pass
        elif symbol.isdigit():
            idx, number = parse_number_stack(text, idx)
            output.append(number)
            unary = False
        elif symbol in ('*', '/'):
            if operators_stack and operators_stack[-1] in ('*', '/', 'u'):
                output.append(operators_stack.pop(-1))
            operators_stack.append(symbol)
            unary = True
        elif symbol in ('+', '-'):
            if unary and symbol == '-':
                operators_stack.append('u')
            else:
                if operators_stack and operators_stack[-1] in ('+', '-', '*', '/', 'u'):
                    output.append(operators_stack.pop(-1))
                operators_stack.append(symbol)
            unary = True
        elif symbol == '(':
            operators_stack.append('(')
            unary = True
        elif symbol == ')':
            while operators_stack[-1] != '(':
                output.append(operators_stack.pop(-1))
            operators_stack.pop(-1)
            unary = False
        else:
            ValueError()
        idx += 1
    while operators_stack:
        output.append(operators_stack.pop(-1))
    return output


def compute_expression_postfix(postfix: list) -> int:
    operands = []
    for token in postfix:
        if type(token) == int:
            operands.append(token)
        elif token == 'u':
            operands.append(-operands.pop())
        elif token in ('+', '-', '*', '/'):
            num_r, num_l = operands.pop(), operands.pop()
            if token == '+':
                operands.append(num_l + num_r)
            elif token == '-':
                operands.append(num_l - num_r)
            elif token == '*':
                operands.append(num_l * num_r)
            elif token == '/':
                operands.append(num_l // num_r)
    return operands.pop()


def postfix_solution(text: str) -> int:
    postfix = parse_expression_postfix(text)
    return compute_expression_postfix(postfix)


def operation_postfix_inplace(operands_stack, operation) -> int:
    if operation == 'u':
        operands_stack.append(-operands_stack.pop())
    elif operation in ('+', '-', '*', '/'):
        num_r, num_l = operands_stack.pop(), operands_stack.pop()
        if operation == '+':
            operands_stack.append(num_l + num_r)
        elif operation == '-':
            operands_stack.append(num_l - num_r)
        elif operation == '*':
            operands_stack.append(num_l * num_r)
        elif operation == '/':
            operands_stack.append(num_l // num_r)
    return operands_stack


def parse_expression_postfix_inplace(text: str) -> int:
    operands_stack = []
    operators_stack = []
    idx = 0
    unary = True
    while idx < len(text):
        symbol = text[idx]
        if symbol == ' ':
            pass
        elif symbol.isdigit():
            idx, number = parse_number_stack(text, idx)
            operands_stack.append(number)
            unary = False
        elif symbol in ('*', '/'):
            if operators_stack and operators_stack[-1] in ('*', '/', 'u'):
                operands_stack = operation_postfix_inplace(operands_stack, operators_stack.pop(-1))
            operators_stack.append(symbol)
            unary = True
        elif symbol in ('+', '-'):
            if unary and symbol == '-':
                operators_stack.append('u')
            else:
                if operators_stack and operators_stack[-1] in ('+', '-', '*', '/', 'u'):
                    operands_stack = operation_postfix_inplace(operands_stack, operators_stack.pop(-1))
                operators_stack.append(symbol)
            unary = True
        elif symbol == '(':
            operators_stack.append('(')
            unary = True
        elif symbol == ')':
            while operators_stack[-1] != '(':
                operands_stack = operation_postfix_inplace(operands_stack, operators_stack.pop(-1))
            operators_stack.pop(-1)
            unary = False
        else:
            ValueError()
        idx += 1
    while operators_stack:
        operands_stack = operation_postfix_inplace(operands_stack, operators_stack.pop(-1))
    return operands_stack[0]


def text_calculator(text: str) -> int:
    # return eval_solution(text)
    # return tree_solution(text)
    # return postfix_solution(text)
    return parse_expression_postfix_inplace(text)


class Test(unittest.TestCase):
    def test_simple_operations(self):
        input_text = "2 + 3"
        expected = 5
        self.assertEqual(expected, text_calculator(input_text))

    def test_simple_operations2(self):
        input_text = "2 - 3"
        expected = -1
        self.assertEqual(expected, text_calculator(input_text))

    def test_simple_operations3(self):
        input_text = "2 * 3"
        expected = 6
        self.assertEqual(expected, text_calculator(input_text))

    def test_simple_operations4(self):
        input_text = "2 / 3"
        expected = 0
        self.assertEqual(expected, text_calculator(input_text))

    def test_simple_operations5(self):
        input_text = "(2 + 3)"
        expected = 5
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases(self):
        input_text = "2 + -3"
        expected = -1
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases2(self):
        input_text = "2"
        expected = 2
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases3(self):
        input_text = "-2"
        expected = -2
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases4(self):
        input_text = "    2    "
        expected = 2
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases5(self):
        input_text = "3 / 3"
        expected = 1
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases6(self):
        input_text = "4 / 3"
        expected = 1
        self.assertEqual(expected, text_calculator(input_text))

    def test_corner_cases7(self):
        input_text = "   (      2    +       3      )      "
        expected = 5
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations(self):
        input_text = "2 + 2 * 2"
        expected = 6
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations1(self):
        input_text = "(2 + 2) * 2"
        expected = 8
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations2(self):
        input_text = "2 + 2 / 4 - 2"
        expected = 0
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations3(self):
        input_text = "(2 + 2) / (4 - 2)"
        expected = 2
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations4(self):
        input_text = "(2 + 2) / 4 - 2"
        expected = -1
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations5(self):
        input_text = "(10000 - 84) * (456 / 450 + 22) + 7 / (34 + 12) + 8 / 34 + 9"
        expected = 228077
        self.assertEqual(expected, text_calculator(input_text))

    def test_advanced_operations6(self):
        input_text = "((((4) * (-1)) + 18 - 7 *(-2)*5/4/(-1)) - 500) / ((-2 * (4) + 5) / 2)"
        expected = 252
        self.assertEqual(expected, text_calculator(input_text))
