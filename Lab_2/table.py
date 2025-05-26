import itertools


def parse_expression(expr):
    """Преобразует выражение в удобный для вычисления формат"""
    expr = expr.replace(' ', '').replace('!', ' not ').replace('∧', ' and ').replace('∨', ' or ')
    expr = expr.replace('>', ' <= ').replace('~', ' == ')
    return expr


def evaluate_expression(expr, variables):
    """Вычисляет значение логического выражения для заданных значений переменных"""
    locals().update(variables)
    try:
        return bool(eval(expr))
    except:
        return None


def get_variables(expr):
    """Извлекает переменные из выражения"""
    variables = set()
    for char in expr:
        if char.islower() and char.isalpha() and char in 'abcde':
            variables.add(char)
    return sorted(variables)


def generate_intermediate_expressions(expr):
    """Генерирует промежуточные выражения для вывода (только корректные)"""
    expr = expr.replace(' ', '')
    parts = []
    stack = []
    current = ""

    for char in expr:
        if char == '(':
            if current:
                stack.append(current)
                current = ""
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                current = stack.pop() + current
            if stack and stack[-1] == '(':
                stack.pop()
            if current:
                test_vars = {v: True for v in get_variables(current)}
                try:
                    parsed = parse_expression(current)
                    evaluate_expression(parsed, test_vars)
                    parts.append(current)
                except:
                    pass

                if stack:
                    current = stack.pop() + '(' + current + ')'
                else:
                    current = '(' + current + ')'
        else:
            current += char

    if current:
        test_vars = {v: True for v in get_variables(current)}
        try:
            parsed = parse_expression(current)
            evaluate_expression(parsed, test_vars)
            parts.append(current)
        except:
            pass

    unique_parts = []
    seen = set()
    for part in parts:
        if part not in seen and part != expr:
            seen.add(part)
            unique_parts.append(part)

    return unique_parts


def generate_truth_table(expr):
    """Генерирует таблицу истинности для логического выражения"""
    variables = get_variables(expr)
    parsed_expr = parse_expression(expr)
    intermediates = generate_intermediate_expressions(expr)

    truth_values = list(itertools.product([0, 1], repeat=len(variables)))

    table = []
    for values in truth_values:
        row = {}
        var_values = {var: bool(val) for var, val in zip(variables, values)}
        row.update({var: int(val) for var, val in var_values.items()})

        locals().update(var_values)
        for part in intermediates:
            try:
                part_expr = parse_expression(part)
                result = evaluate_expression(part_expr, var_values)
                if result is not None:
                    row[part] = int(result)
            except:
                pass

        result = evaluate_expression(parsed_expr, var_values)
        row[expr] = int(result) if result is not None else '?'

        table.append(row)

    return table, variables, intermediates


def build_sdnf(table, variables, expr):
    """Строит СДНФ из таблицы истинности"""
    sdnf_terms = []
    numeric_form = []

    for i, row in enumerate(table):
        if row[expr]:
            term = []
            for var in variables:
                if not row[var]:
                    term.append(f"(!{var})")
                else:
                    term.append(var)
            sdnf_terms.append("&".join(term))
            numeric_form.append(i)

    if not sdnf_terms:
        return "Не существует (функция всегда ложна)", []

    sdnf = "|".join([f"({term})" for term in sdnf_terms])
    return sdnf, numeric_form


def build_sknf(table, variables, expr):
    """Строит СКНФ из таблицы истинности"""
    sknf_terms = []
    numeric_form = []

    for i, row in enumerate(table):
        if not row[expr]:
            term = []
            for var in variables:
                if row[var]:
                    term.append(f"(!{var})")
                else:
                    term.append(var)
            sknf_terms.append("|".join(term))
            numeric_form.append(i)

    if not sknf_terms:
        return "Не существует (функция всегда истинна)", []

    sknf = "&".join([f"({term})" for term in sknf_terms])
    return sknf, numeric_form


def calculate_index_form(table, expr):
    """Вычисляет индексную форму функции"""
    index = 0
    for i, row in enumerate(table):
        if row[expr]:
            index += 2 ** (len(table) - i - 1)
    return index


def print_truth_table(table, variables, intermediates, expr):
    """Печатает таблицу истинности в заданном формате"""
    columns = variables.copy()

    for part in intermediates:
        if part in table[0]:
            columns.append(part)
    columns.append(expr)

    col_widths = {col: max(len(col), 1) for col in columns}
    for col in columns:
        for row in table:
            col_widths[col] = max(col_widths[col], len(str(row[col])))

    header = " | ".join([col.center(col_widths[col]) for col in columns])
    print(header)

    print("-" * len(header))

    for row in table:
        row_str = " | ".join([str(row[col]).center(col_widths[col]) for col in columns])
        print(row_str)

