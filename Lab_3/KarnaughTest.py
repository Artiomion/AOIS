import unittest
from BooleanExpression import BooleanExpression
from Karnaugh2 import Karnaugh2
from Karnaugh3 import Karnaugh3
from Karnaugh4 import Karnaugh4
from Karnaugh5 import Karnaugh5


class TestKarnaughMethod(unittest.TestCase):
    def test_Karnaugh2_SDNF(self):
        self.exp = BooleanExpression('(a>b)')
        karnaugh_method = Karnaugh2(self.exp, 'SDNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '((!a)|b)')

    def test_Karnaugh2_SKNF(self):
        self.exp = BooleanExpression('(a>b)')
        karnaugh_method = Karnaugh2(self.exp, 'SKNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '((!a)|b)')

    def test_Karnaugh3_SDNF(self):
        self.exp = BooleanExpression('(a>(b&c))')
        karnaugh_method = Karnaugh3(self.exp, 'SDNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '((!a)|(b&c))')

    def test_Karnaugh3_SKNF(self):
        self.exp = BooleanExpression('(a>(b&c))')
        karnaugh_method = Karnaugh3(self.exp, 'SKNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '(((!a)|b)&((!a)|c))')

    def test_Karnaugh4_SDNF(self):
        self.exp = BooleanExpression('(a>(b&(c|d)))')
        karnaugh_method = Karnaugh4(self.exp, 'SDNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '((!a)|(b&d)|(b&c))')

    def test_Karnaugh4_SKNF(self):
        self.exp = BooleanExpression('(a>(b&(c|d)))')
        karnaugh_method = Karnaugh4(self.exp, 'SKNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '(((!a)|c|d)&((!a)|b))')

    def test_Karnaugh5_SDNF(self):
        self.exp = BooleanExpression('((a>b)&(c~(d|e)))')
        karnaugh_method = Karnaugh5(self.exp, 'SDNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '(((!a)&(!c)&(!d)&(!e))|((!a)&c&d)|((!a)&c&e)|(b&(!c)&(!d)&(!e))|(b&c&d)|(b&c&e))')

    def test_Karnaugh5_SKNF(self):
        self.exp = BooleanExpression('((a>b)&(c~(d|e)))')
        karnaugh_method = Karnaugh5(self.exp, 'SKNF')
        merged_form = karnaugh_method.merged_form()
        self.assertEqual(merged_form, '((c|(!e))&(c|(!d))&((!c)|d|e)&((!a)|b))')
