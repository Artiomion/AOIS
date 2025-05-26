import unittest
from table import (parse_expression, get_variables, evaluate_expression,
                   generate_intermediate_expressions, generate_truth_table,
                   build_sdnf, build_sknf, calculate_index_form)

class TestLogicFunctions(unittest.TestCase):
    def test_parse_expression(self):
        self.assertEqual(parse_expression("a∧b"), "a and b")
        self.assertEqual(parse_expression("a∨b"), "a or b")
        self.assertEqual(parse_expression("!a"), " not a")
        self.assertEqual(parse_expression("a>b"), "a <= b")
        self.assertEqual(parse_expression("a~b"), "a == b")
        self.assertEqual(parse_expression("a ∧ (b ∨ c)"), "a and (b or c)")

    def test_get_variables(self):
        self.assertEqual(get_variables("a∧b∨c"), ['a', 'b', 'c'])
        self.assertEqual(get_variables("(a>b)~c"), ['a', 'b', 'c'])
        self.assertEqual(get_variables("!a∧!b"), ['a', 'b'])
        self.assertEqual(get_variables("x∨y"), [])  # только a-e поддерживаются

    def test_evaluate_expression(self):
        self.assertTrue(evaluate_expression("a and b", {'a': True, 'b': True}))
        self.assertFalse(evaluate_expression("a or b", {'a': False, 'b': False}))
        self.assertTrue(evaluate_expression("a == b", {'a': True, 'b': True}))
        self.assertFalse(evaluate_expression("a <= b", {'a': True, 'b': False}))

    def test_generate_intermediate_expressions(self):
        self.assertCountEqual(generate_intermediate_expressions("a∧b"), [])
        self.assertCountEqual(generate_intermediate_expressions("(a∧b)∨c"), ["a∧b"])
        self.assertCountEqual(generate_intermediate_expressions("(a∨b)∧(c>d)"), ["a∨b", "c>d"])

    def test_generate_truth_table(self):
        # Простая таблица для a ∧ b
        table, vars, _ = generate_truth_table("a∧b")
        self.assertEqual(vars, ['a', 'b'])
        self.assertEqual(len(table), 4)
        self.assertEqual(table[0], {'a': 0, 'b': 0, 'a∧b': 0})
        self.assertEqual(table[3], {'a': 1, 'b': 1, 'a∧b': 1})

        # Таблица с промежуточными выражениями
        table, vars, parts = generate_truth_table("(a∨b)∧c")
        self.assertIn("a∨b", parts)
        self.assertEqual(len(table), 8)  # 3 переменные = 8 строк

    def test_build_sdnf(self):
        table, vars, _ = generate_truth_table("a∧b")
        sdnf, nums = build_sdnf(table, vars, "a∧b")
        self.assertEqual(sdnf, "(a&b)")
        self.assertEqual(nums, [3])

        table, vars, _ = generate_truth_table("a∨b")
        sdnf, nums = build_sdnf(table, vars, "a∨b")
        self.assertEqual(sdnf, "((!a)&b)|(a&(!b))|(a&b)")
        self.assertEqual(nums, [1, 2, 3])

    def test_build_sknf(self):
        table, vars, _ = generate_truth_table("a∧b")
        sknf, nums = build_sknf(table, vars, "a∧b")
        self.assertEqual(sknf, "(a|b)&(a|(!b))&((!a)|b)")
        self.assertEqual(nums, [0, 1, 2])

        table, vars, _ = generate_truth_table("a∨b")
        sknf, nums = build_sknf(table, vars, "a∨b")
        self.assertEqual(sknf, "(a|b)")
        self.assertEqual(nums, [0])

    def test_calculate_index_form(self):
        table, _, _ = generate_truth_table("a∧b")
        index = calculate_index_form(table, "a∧b")
        self.assertEqual(index, 1)  # 1000 в двоичной (только последняя строка истинна)

        table, _, _ = generate_truth_table("a∨b")
        index = calculate_index_form(table, "a∨b")
        self.assertEqual(index, 7)  # 1110 в двоичной (первые три строки истинны)

    def test_parse_complex_expression(self):
        self.assertEqual(parse_expression("(a∧b)∨(c>d)"), "(a and b) or (c <= d)")
        self.assertEqual(parse_expression("!(a∨b)~c"), " not (a or b) == c")
        self.assertEqual(parse_expression("a∧b∧c∧d"), "a and b and c and d")

    def test_evaluate_complex_expression(self):
        self.assertTrue(evaluate_expression("not (a or b)", {'a': False, 'b': False}))
        self.assertFalse(evaluate_expression("(a and b) == (c or d)",
                                             {'a': True, 'b': True, 'c': False, 'd': False}))
        self.assertTrue(evaluate_expression("(a <= b) or (c == d)",
                                            {'a': False, 'b': True, 'c': True, 'd': True}))

    def test_truth_table_complex(self):
        # Тест для выражения с 4 переменными
        table, vars, parts = generate_truth_table("(a∧b)∨(c∧d)")
        self.assertEqual(vars, ['a', 'b', 'c', 'd'])
        self.assertEqual(len(table), 16)
        self.assertIn("a∧b", parts)
        self.assertIn("c∧d", parts)

        # Проверка конкретных строк
        self.assertEqual(table[0]['(a∧b)∨(c∧d)'], 0)
        self.assertEqual(table[15]['(a∧b)∨(c∧d)'], 1)

    def test_sdnf_sknf_edge_cases(self):
        # Тест для всегда истинного выражения
        table, vars, _ = generate_truth_table("a∨(!a)")
        sdnf, sdnf_nums = build_sdnf(table, vars, "a∨(!a)")
        sknf, sknf_nums = build_sknf(table, vars, "a∨(!a)")
        self.assertEqual(sdnf, "((!a))|(a)")
        self.assertEqual(sknf, "Не существует (функция всегда истинна)")

        # Тест для всегда ложного выражения
        table, vars, _ = generate_truth_table("a∧(!a)")
        sdnf, sdnf_nums = build_sdnf(table, vars, "a∧(!a)")
        sknf, sknf_nums = build_sknf(table, vars, "a∧(!a)")
        self.assertEqual(sdnf, "Не существует (функция всегда ложна)")
        self.assertEqual(sknf, "(a)&((!a))")

    def test_index_form_edge_cases(self):
        # Всегда истинное выражение
        table, _, _ = generate_truth_table("a∨!a")
        index = calculate_index_form(table, "a∨!a")
        self.assertEqual(index, 3)  # Для 2 переменных: 11 в двоичной

        # Всегда ложное выражение
        table, _, _ = generate_truth_table("a∧!a")
        index = calculate_index_form(table, "a∧!a")
        self.assertEqual(index, 0)

        # Проверка для 3 переменных
        table, _, _ = generate_truth_table("a∧b∧c")
        index = calculate_index_form(table, "a∧b∧c")
        self.assertEqual(index, 1)  # Только последняя строка истинна

if __name__ == '__main__':
    unittest.main()