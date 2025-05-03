import unittest
from BooleanExpression import BooleanExpression


class TestBooleanExpression(unittest.TestCase):

    def setUp(self):
        self.expression = BooleanExpression('((a&b)|(!c))')

    def test_create_syntax_tree(self):
        syntax_tree = self.expression.create_syntax_tree('((a&b)|(!c))')
        self.assertIsNotNone(syntax_tree)
        # Add more specific assertions if needed

    def test_calculate(self):
        interpretation1 = self.expression.calculate(self.expression.create_syntax_tree('((a&b)|(!c))'),
                                           [True, False, True], '((a&b)|(!c))')
        interpretation2 = self.expression.calculate(self.expression.create_syntax_tree('((a&b)|(!c))'),
                                           [True, False, False], '((a&b)|(!c))')
        self.assertEqual(interpretation1, False)
        self.assertEqual(interpretation2, True)

    def test_build_SDNF(self):
        expression = BooleanExpression('((a&b)|(!c))')
        self.assertEqual(expression.build_SDNF(), '((!a)&(!b)&(!c))|((!a)&b&(!c))|(a&(!b)&(!c))|(a&b&(!c))|(a&b&c)')

    def test_build_SKNF(self):
        expression = BooleanExpression('((a&b)|(!c))')
        self.assertEqual(expression.build_SKNF(), '(a|b|(!c))&(a|(!b)|(!c))&((!a)|b|(!c))')

    def test_print_numeric_forms(self):
        expression = BooleanExpression('((a&b)|(!c))')
        SDNF, SKNF = expression.build_numeric_forms()
        self.assertEqual(SDNF, '(0 2 4 6 7 ) |')
        self.assertEqual(SKNF, '(1 3 5 ) &')

    def test_print_index_form(self):
        expression = BooleanExpression('((a&b)|(!c))')
        self.assertEqual(expression.build_index_form(), '171 - 10101011')


if __name__ == '__main__':
    unittest.main()
