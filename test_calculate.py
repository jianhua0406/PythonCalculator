from unittest import TestCase

from calculate import *


class TestCalculate(TestCase):
    def test_operator_compare(self):
        test = {
            ('+', '-', 0),
            ('-', '-', 0),
            ('-', '+', 0),
            ('*', '-', 1),
            ('+', '/', -1),
            ('*', '%', 0),
        }
        for sig1, sig2, res in test:
            self.assertEqual(operator_compare(sig1, sig2), res)

    def test_string_to_signals(self):
        self.assertEqual(string_to_signals('12+34*56%78/90'), [12, '+', 34, '*', 56, '%', 78, '/', 90])

        self.assertEqual(string_to_signals('1*2+3'), [1, '*', 2, '+', 3])
        self.assertEqual(string_to_signals('1+2*3'), [1, '+', 2, '*', 3])
        self.assertEqual(string_to_signals('(1+2)*(3*4)'), ['(', 1, '+', 2, ')', '*', '(', 3, '*', 4, ')'])

    def test_infix_to_suffix(self):
        self.assertEqual(infix_to_suffix(string_to_signals('1*2+3')), [1, 2, '*', 3, '+'])
        self.assertEqual(infix_to_suffix(string_to_signals('1+2*3')), [1, 2, 3, '*', '+'])
        self.assertEqual(infix_to_suffix(string_to_signals('(1+2)*(3*4)')), [1, 2, '+', 3, 4, '*', '*'])

    def test_suffix_calculate(self):
        self.assertEqual(suffix_calculate([1, 2, '*', 3, '+']), 5)
        self.assertEqual(suffix_calculate([1, 2, 3, '*', '+']), 7)
        self.assertEqual(suffix_calculate([1, 2, '+', 3, 4, '*', '*']), 36)

    def test_calculate_string(self):
        self.assertEqual(calculate_string('1*2+3'), 5)
        self.assertEqual(calculate_string('1+2*3'), 7)
        self.assertEqual(calculate_string('(1+2)*(3*4)'), 36)
