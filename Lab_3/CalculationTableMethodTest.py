import unittest
from CalculationTableMethod import CalculationTableMethod, CalculationMethod, BooleanExpression


class TestCalculationMethodNormalForm(unittest.TestCase):
    def test_SDNF_1(self):
        self.exp = BooleanExpression('(a|(r&(!s)))')
        calculation_method = CalculationMethod(self.exp.build_SDNF(), 'SDNF')
        calculation_table_method = CalculationTableMethod(calculation_method)
        calculation_table_method.merge()
        merged_form = calculation_table_method.merged_form()
        calculation_table_method.build_table()
        self.assertEqual(merged_form, '(a|(r&(!s)))')

    def test_SDNF_2(self):
        self.exp = BooleanExpression('(a&(b>(c|d)))')
        calculation_method = CalculationMethod(self.exp.build_SDNF(), 'SDNF')
        calculation_table_method = CalculationTableMethod(calculation_method)
        calculation_table_method.merge()
        merged_form = calculation_table_method.merged_form()
        self.assertEqual(merged_form, '((a&(!b))|((a&d)|(a&c)))')

    def test_SKNF_1(self):
        self.exp = BooleanExpression('(a|(r&(!s)))')
        calculation_method = CalculationMethod(self.exp.build_SKNF(), 'SKNF')
        calculation_table_method = CalculationTableMethod(calculation_method)
        calculation_table_method.merge()
        merged_form = calculation_table_method.merged_form()
        self.assertEqual(merged_form, '((a|r)&(a|(!s)))')

    def test_SKNF_2(self):
        self.exp = BooleanExpression('(a&(b>(c|d)))')
        calculation_method = CalculationMethod(self.exp.build_SKNF(), 'SKNF')
        calculation_table_method = CalculationTableMethod(calculation_method)
        calculation_table_method.merge()
        merged_form = calculation_table_method.merged_form()
        self.assertEqual(merged_form, '(a&((!b)|(c|d)))')
