import unittest
from table import generate_truth_table, build_sdnf, build_sknf, parse_expression, get_variables, evaluate_expression, \
    generate_intermediate_expressions, calculate_index_form
from calculus_method import minimize_sdnf_calculus, minimize_sknf_calculus
from karnaugh_map import create_karnaugh_map, minimize_sdnf_karnaugh, minimize_sknf_karnaugh, find_groups, \
    group_to_term, print_karnaugh_map
from table_calculus_method import minimize_sdnf_table_calculus, minimize_sknf_table_calculus


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
        table, vars, parts = generate_truth_table("(a∧b)∨(c∧d)")
        self.assertEqual(vars, ['a', 'b', 'c', 'd'])
        self.assertEqual(len(table), 16)
        self.assertIn("a∧b", parts)
        self.assertIn("c∧d", parts)

        self.assertEqual(table[0]['(a∧b)∨(c∧d)'], 0)
        self.assertEqual(table[15]['(a∧b)∨(c∧d)'], 1)

    def test_sdnf_sknf_edge_cases(self):
        table, vars, _ = generate_truth_table("a∨(!a)")
        sdnf, sdnf_nums = build_sdnf(table, vars, "a∨(!a)")
        sknf, sknf_nums = build_sknf(table, vars, "a∨(!a)")
        self.assertEqual(sdnf, "((!a))|(a)")
        self.assertEqual(sknf, "Не существует (функция всегда истинна)")

        table, vars, _ = generate_truth_table("a∧(!a)")
        sdnf, sdnf_nums = build_sdnf(table, vars, "a∧(!a)")
        sknf, sknf_nums = build_sknf(table, vars, "a∧(!a)")
        self.assertEqual(sdnf, "Не существует (функция всегда ложна)")
        self.assertEqual(sknf, "(a)&((!a))")

    def test_index_form_edge_cases(self):
        table, _, _ = generate_truth_table("a∨!a")
        index = calculate_index_form(table, "a∨!a")
        self.assertEqual(index, 3)

        table, _, _ = generate_truth_table("a∧!a")
        index = calculate_index_form(table, "a∧!a")
        self.assertEqual(index, 0)

        table, _, _ = generate_truth_table("a∧b∧c")
        index = calculate_index_form(table, "a∧b∧c")
        self.assertEqual(index, 1)

class TestTruthTable(unittest.TestCase):
    def test_simple_expression(self):
        expr = "a ∧ b"
        table, variables, intermediates = generate_truth_table(expr)
        self.assertEqual(variables, ['a', 'b'])
        self.assertEqual(len(table), 4)


        expected = [
            {'a': 0, 'b': 0, 'a∧b': 0},
            {'a': 0, 'b': 1, 'a∧b': 0},
            {'a': 1, 'b': 0, 'a∧b': 0},
            {'a': 1, 'b': 1, 'a∧b': 1},
        ]

        for i, row in enumerate(table):
            self.assertEqual(row['a'], expected[i]['a'])
            self.assertEqual(row['b'], expected[i]['b'])
            self.assertEqual(row[expr], expected[i]['a∧b'])

    def test_three_variable_expression(self):
        expr = "(a ∨ b) ∧ !c"
        table, variables, _ = generate_truth_table(expr)
        self.assertEqual(variables, ['a', 'b', 'c'])
        self.assertEqual(len(table), 8)


        self.assertEqual(table[0][expr], 0)
        self.assertEqual(table[3][expr], 0)
        self.assertEqual(table[6][expr], 1)


class TestSDNFSKNFConstruction(unittest.TestCase):
    def test_sdnf_construction(self):
        expr = "a ∧ b"
        table, variables, _ = generate_truth_table(expr)
        sdnf, numeric = build_sdnf(table, variables, expr)
        self.assertEqual(numeric, [3])
        self.assertEqual(sdnf, "(a&b)")

    def test_sknf_construction(self):
        expr = "a ∨ b"
        table, variables, _ = generate_truth_table(expr)
        sknf, numeric = build_sknf(table, variables, expr)
        self.assertEqual(numeric, [0])
        self.assertEqual(sknf, "(a|b)")

    def test_always_true(self):
        expr = "a ∨ !a"
        table, variables, _ = generate_truth_table(expr)
        sknf, numeric = build_sknf(table, variables, expr)
        self.assertEqual(sknf, "Не существует (функция всегда истинна)")

    def test_always_false(self):
        expr = "a ∧ !a"
        table, variables, _ = generate_truth_table(expr)
        sdnf, numeric = build_sdnf(table, variables, expr)
        self.assertEqual(sdnf, "Не существует (функция всегда ложна)")


class TestCalculusMethod(unittest.TestCase):
    def test_sdnf_minimization(self):
        sdnf = "(a&b&c)|(a&b&!c)|(a&!b&c)"
        variables = ['a', 'b', 'c']
        minimized, _ = minimize_sdnf_calculus(sdnf, variables)
        self.assertEqual(minimized, "(a&b)|(a&c)")

    def test_sknf_minimization(self):
        sknf = "(a|b|c)&(a|b|!c)&(a|!b|c)"
        variables = ['a', 'b', 'c']
        minimized, _ = minimize_sknf_calculus(sknf, variables)
        self.assertEqual(minimized, "(a|b)&(a|c)")

    def test_no_minimization_possible(self):
        sdnf = "(a&b)|(!a&!b)"
        variables = ['a', 'b']
        minimized, _ = minimize_sdnf_calculus(sdnf, variables)
        self.assertEqual(minimized, "(a&b)|(!a&!b)")


class TestTableCalculusMethod(unittest.TestCase):
    def test_sdnf_table_minimization(self):
        sdnf = "(a&b&c)|(a&b&!c)|(a&!b&c)"
        numeric = [7, 6, 5]  # 111, 110, 101
        variables = ['a', 'b', 'c']
        minimized, _ = minimize_sdnf_table_calculus(sdnf, variables, numeric)
        self.assertEqual(minimized, "(a&b)|(a&c)")

    def test_sknf_table_minimization(self):
        sknf = "(a|b|c)&(a|b|!c)&(a|!b|c)"
        numeric = [0, 1, 2]  # 000, 001, 010
        variables = ['a', 'b', 'c']
        minimized, _ = minimize_sknf_table_calculus(sknf, variables, numeric)
        self.assertEqual(minimized, "(a|b)&(a|c)")


class TestKarnaughMap(unittest.TestCase):
    def test_karnaugh_map_creation(self):
        expr = "a ∧ b"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        kmap, vars_, rows, cols = kmap_data
        self.assertEqual(vars_, ['a', 'b'])
        self.assertEqual(kmap[('0', '0')], 0)
        self.assertEqual(kmap[('1', '1')], 1)

    def test_sdnf_karnaugh_minimization(self):
        expr = "(a ∧ b) ∨ (a ∧ !b) ∨ (!a ∧ b)"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        minimized, _ = minimize_sdnf_karnaugh(kmap_data, variables)
        self.assertEqual(minimized, "(a)|(b)")

    def test_sknf_karnaugh_minimization(self):
        expr = "(a ∨ b) ∧ (a ∨ !b) ∧ (!a ∨ b)"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        minimized, _ = minimize_sknf_karnaugh(kmap_data, variables)
        self.assertEqual(minimized, "(a)&(b)")


class TestIntegration(unittest.TestCase):
    def test_full_workflow(self):
        expr = "(a ∧ b) ∨ (a ∧ !b ∧ c)"
        table, variables, _ = generate_truth_table(expr)

        sdnf, sdnf_numeric = build_sdnf(table, variables, expr)
        sknf, sknf_numeric = build_sknf(table, variables, expr)

        min_sdnf_calc, _ = minimize_sdnf_calculus(sdnf, variables)
        self.assertEqual(min_sdnf_calc, "(a&c)|(a&b)")

        min_sdnf_table, _ = minimize_sdnf_table_calculus(sdnf, variables, sdnf_numeric)
        self.assertEqual(min_sdnf_table, "(a&c)|(a&b)")

        kmap_data = create_karnaugh_map(table, variables, expr)
        min_sdnf_karnaugh, _ = minimize_sdnf_karnaugh(kmap_data, variables)
        self.assertEqual(min_sdnf_karnaugh, "(a&c)|(a&b)")


class TestKarnaughMap(unittest.TestCase):
    def test_create_karnaugh_2vars(self):
        expr = "a ∧ b"
        table, variables, _ = generate_truth_table(expr)
        kmap, vars_, rows, cols = create_karnaugh_map(table, variables, expr)

        self.assertEqual(kmap[('0', '0')], 0)
        self.assertEqual(kmap[('0', '1')], 0)
        self.assertEqual(kmap[('1', '0')], 0)
        self.assertEqual(kmap[('1', '1')], 1)
        self.assertEqual(rows, ['0', '1'])
        self.assertEqual(cols, ['0', '1'])

    def test_create_karnaugh_3vars(self):
        expr = "(a ∧ b) ∨ c"
        table, variables, _ = generate_truth_table(expr)
        kmap, vars_, rows, cols = create_karnaugh_map(table, variables, expr)

        self.assertEqual(kmap[('0', '00')], 0)
        self.assertEqual(kmap[('0', '11')], 1)
        self.assertEqual(kmap[('1', '01')], 1)
        self.assertEqual(cols, ['00', '01', '11', '10'])

    def test_create_karnaugh_4vars(self):
        expr = "a ∧ (b ∨ (c ∧ d))"
        table, variables, _ = generate_truth_table(expr)
        kmap, vars_, rows, cols = create_karnaugh_map(table, variables, expr)

        self.assertEqual(len(rows), 4)
        self.assertEqual(len(cols), 4)
        self.assertEqual(kmap[('00', '11')], 0)
        self.assertEqual(kmap[('11', '11')], 1)

    def test_find_groups(self):
        kmap = {
            ('0', '0'): 0, ('0', '1'): 1,
            ('1', '0'): 0, ('1', '1'): 1
        }
        groups = find_groups(kmap, ['0', '1'], ['0', '1'], 2, value=1)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 2)

        kmap = {
            ('00', '00'): 0, ('00', '01'): 1, ('00', '11'): 1, ('00', '10'): 0,
            ('01', '00'): 0, ('01', '01'): 1, ('01', '11'): 1, ('01', '10'): 0,
            ('11', '00'): 0, ('11', '01'): 0, ('11', '11'): 1, ('11', '10'): 0,
            ('10', '00'): 0, ('10', '01'): 0, ('10', '11'): 0, ('10', '10'): 0
        }
        groups = find_groups(kmap, ['00', '01', '11', '10'], ['00', '01', '11', '10'], 4, value=1)
        self.assertEqual(len(groups), 2)
        self.assertTrue(any(len(g) == 4 for g in groups))

    def test_group_to_term(self):
        variables = ['a', 'b', 'c', 'd']

        group = [('01', '01'), ('01', '11'), ('11', '01'), ('11', '11')]
        term = group_to_term(group, variables, 4, value=1)
        self.assertEqual(term, "b&d")

        group = [('00', '00'), ('10', '00')]
        term = group_to_term(group, variables, 4, value=0)
        self.assertEqual(term, "b|c|d")

    def test_minimize_sdnf_karnaugh_complex(self):
        expr = "(!a ∧ !b ∧ !c) ∨ (!a ∧ b ∧ !c) ∨ (a ∧ !b ∧ c) ∨ (a ∧ b ∧ c)"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        minimized, _ = minimize_sdnf_karnaugh(kmap_data, variables)
        self.assertEqual(minimized, "(!a&!c)|(a&c)")

    def test_minimize_sknf_karnaugh_complex(self):
        expr = "(a ∨ b ∨ !c) ∧ (a ∨ !b ∨ !c) ∧ (!a ∨ b ∨ c) ∧ (!a ∨ !b ∨ c)"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        minimized, _ = minimize_sknf_karnaugh(kmap_data, variables)
        self.assertEqual(minimized, "(a|!c)&(!a|c)")

    def test_karnaugh_edge_cases(self):
        expr = "a ∨ !a"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        minimized, _ = minimize_sdnf_karnaugh(kmap_data, variables)
        self.assertEqual(minimized, "(!a)|(a)")

        expr = "a ∧ !a"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)
        minimized, _ = minimize_sknf_karnaugh(kmap_data, variables)
        self.assertEqual(minimized, "(a)&(!a)")

    def test_group_to_term_single_variable(self):
        variables = ['a']

        term = group_to_term([('0', '0')], variables, 1, value=1)
        self.assertEqual(term, "!a")

        term = group_to_term([('1', '0')], variables, 1, value=1)
        self.assertEqual(term, "a")

        term = group_to_term([('0', '0')], variables, 1, value=0)
        self.assertEqual(term, "a")
        term = group_to_term([('1', '0')], variables, 1, value=0)
        self.assertEqual(term, "!a")

    def test_group_to_term_two_variables(self):
        variables = ['a', 'b']

        term = group_to_term([('0', '1')], variables, 2, value=1)
        self.assertEqual(term, "!a&b")

        term = group_to_term([('0', '0'), ('0', '1')], variables, 2, value=1)
        self.assertEqual(term, "!a")

        term = group_to_term([('0', '1'), ('1', '1')], variables, 2, value=1)
        self.assertEqual(term, "b")

        term = group_to_term([('0', '0'), ('0', '1'), ('1', '0'), ('1', '1')], variables, 2, value=1)
        self.assertEqual(term, "")

    def test_group_to_term_three_variables(self):
        variables = ['a', 'b', 'c']

        term = group_to_term([('1', '01')], variables, 3, value=1)
        self.assertEqual(term, "a&!b&c")

        term = group_to_term([('0', '11'), ('1', '11')], variables, 3, value=1)
        self.assertEqual(term, "b&c")

        term = group_to_term([('0', '00'), ('0', '01'), ('1', '00'), ('1', '01')], variables, 3, value=1)
        self.assertEqual(term, "!b")

        term = group_to_term([('0', '10'), ('1', '10')], variables, 3, value=0)
        self.assertEqual(term, "!b|c")

    def test_group_to_term_four_variables(self):
        variables = ['a', 'b', 'c', 'd']

        term = group_to_term([('00', '00'), ('00', '01'), ('01', '00'), ('01', '01')], variables, 4, value=1)
        self.assertEqual(term, "!a&!c")

        term = group_to_term([('00', '11'), ('01', '11'), ('10', '11'), ('11', '11')], variables, 4, value=1)
        self.assertEqual(term, "c&d")

        term = group_to_term([('11', '00'), ('11', '01'), ('11', '11'), ('11', '10')], variables, 4, value=1)
        self.assertEqual(term, "a&b")

        group = [('00', '00'), ('00', '01'), ('00', '11'), ('00', '10'),
                 ('10', '00'), ('10', '01'), ('10', '11'), ('10', '10')]
        term = group_to_term(group, variables, 4, value=1)
        self.assertEqual(term, "!b")

    def test_group_to_term_five_variables(self):
        variables = ['a', 'b', 'c', 'd', 'e']

        group = [('00', '000'), ('00', '010'), ('01', '000'), ('01', '010')]
        term = group_to_term(group, variables, 5, value=1)
        self.assertEqual(term, "!a&!c&!e")

        group = [('00', '000'), ('00', '001'), ('00', '011'), ('00', '010'),
                 ('01', '000'), ('01', '001'), ('01', '011'), ('01', '010')]
        term = group_to_term(group, variables, 5, value=1)
        self.assertEqual(term, "!a&!c")

    def test_group_to_term_special_forms(self):
        variables = ['a', 'b']

        term = group_to_term([('0', '1'), ('1', '1')], variables, 2, value=1)
        self.assertEqual(term, "b")

        term = group_to_term([('0', '1'), ('1', '1')], variables, 2, value=0)
        self.assertEqual(term, "!b")

        all_cells = [('0', '0'), ('0', '1'), ('1', '0'), ('1', '1')]
        term_sdnf = group_to_term(all_cells, variables, 2, value=1)
        term_sknf = group_to_term(all_cells, variables, 2, value=0)
        self.assertEqual(term_sdnf, "")
        self.assertEqual(term_sknf, "")

    def test_group_to_term_with_negations(self):
        variables = ['a', 'b', 'c']

        term = group_to_term([('0', '01'), ('0', '11')], variables, 3, value=1)
        self.assertEqual(term, "!a&c")

        term = group_to_term([('0', '01'), ('1', '01')], variables, 3, value=1)
        self.assertEqual(term, "!b&c")

class TestKarnaughPrinting(unittest.TestCase):
    def test_print_karnaugh(self):
        expr = "a ∧ b"
        table, variables, _ = generate_truth_table(expr)
        kmap_data = create_karnaugh_map(table, variables, expr)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            print_karnaugh_map(*kmap_data)
        output = f.getvalue()

if __name__ == '__main__':
    unittest.main()