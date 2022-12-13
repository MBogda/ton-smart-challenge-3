import unittest


def text_calculator(text: str) -> str:
    return str(eval(text.replace("/", "//")))


class Test(unittest.TestCase):
    def test_simple_operations(self):
        input_text = "2 + 3"
        expected = "5"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "2 - 3"
        expected = "-1"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "2 * 3"
        expected = "6"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "2 / 3"
        expected = "0"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "(2 + 3)"
        expected = "5"
        self.assertEqual(text_calculator(input_text), expected)

    def test_corner_cases(self):
        input_text = "2 + -3"
        expected = "-1"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "2"
        expected = "2"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "-2"
        expected = "-2"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "3 / 3"
        expected = "1"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "4 / 3"
        expected = "1"
        self.assertEqual(text_calculator(input_text), expected)

    def test_advanced_operations(self):
        input_text = "2 + 2 * 2"
        expected = "6"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "(2 + 2) * 2"
        expected = "8"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "2 + 2 / 4 - 2"
        expected = "0"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "(2 + 2) / (4 - 2)"
        expected = "2"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "(2 + 2) / 4 - 2"
        expected = "-1"
        self.assertEqual(text_calculator(input_text), expected)

        input_text = "(10000 - 84) * (456 / 450 + 22) + 7 / (34 + 12) + 8 / 34 + 9"
        expected = "228077"
        self.assertEqual(text_calculator(input_text), expected)
