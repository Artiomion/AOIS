import itertools
from calculus_method import parse_term, can_glue, absorb


def create_karnaugh_map(table, variables, expr):
    num_vars = len(variables)
    if num_vars > 5:
        return "Карта Карно поддерживает до 5 переменных."

    gray_code_2 = ['00', '01', '11', '10']
    gray_code_3 = ['000', '001', '011', '010', '110', '111', '101', '100']
    kmap = {}

    if num_vars == 1:
        rows, cols = ['0', '1'], ['0']
    elif num_vars == 2:
        rows, cols = ['0', '1'], ['0', '1']
    elif num_vars == 3:
        rows, cols = ['0', '1'], gray_code_2
    elif num_vars == 4:
        rows, cols = gray_code_2, gray_code_2
    else:  # num_vars == 5
        rows, cols = gray_code_2, gray_code_3

    for row in rows:
        for col in cols:
            kmap[(row, col)] = 0

    for row in table:
        binary = ''
        for var in variables:
            binary += str(row[var])
        if num_vars == 1:
            row_idx, col_idx = binary, '0'
        elif num_vars == 2:
            row_idx, col_idx = binary[0], binary[1]
        elif num_vars == 3:
            row_idx, col_idx = binary[0], binary[1:]
        elif num_vars == 4:
            row_idx, col_idx = binary[:2], binary[2:]
        else:  # num_vars == 5
            row_idx, col_idx = binary[:2], binary[2:]
        kmap[(row_idx, col_idx)] = row[expr]

    return kmap, variables, rows, cols


def print_karnaugh_map(kmap, variables, rows, cols):
    num_vars = len(variables)
    print("\nКарта Карно:")

    # Формируем заголовок
    if num_vars == 1:
        header = "  | " + " ".join(cols)
        print("  ".join(variables[:1]) + " \\")
    elif num_vars == 2:
        header = "  | " + " ".join(cols)
        print("  ".join(variables[:1]) + " \\" + " ".join(variables[1:]))
    elif num_vars == 3:
        header = "  | " + " ".join(cols)
        print("  ".join(variables[:1]) + " \\" + " ".join(variables[1:]))
    elif num_vars == 4:
        header = "  | " + " ".join(cols)
        print(" ".join(variables[:2]) + " \\" + " ".join(variables[2:]))
    else:  # num_vars == 5
        header = "  | " + " ".join(cols)
        print(" ".join(variables[:2]) + " \\" + " ".join(variables[2:]))

    print(header)
    print("-" * len(header))

    for row in rows:
        row_str = row + " | " + " ".join(str(kmap[(row, col)]) for col in cols)
        print(row_str)


def find_groups(kmap, rows, cols, num_vars, value=1):
    """Находит группы единиц (для СДНФ) или нулей (для СКНФ) в карте Карно."""
    groups = []
    covered = set()

    group_sizes = [(2, 4), (2, 2), (1, 4), (2, 1), (1, 2), (1, 1)] if num_vars == 4 else \
        [(2, 4), (1, 4), (2, 2), (1, 2), (2, 1), (1, 1)] if num_vars == 5 else \
            [(2, 2), (1, 2), (2, 1), (1, 1)] if num_vars == 3 else \
                [(1, 2), (2, 1), (1, 1)] if num_vars == 2 else [(1, 1)]

    for size_r, size_c in group_sizes:
        for i in range(len(rows)):
            for j in range(len(cols)):
                group = []
                valid = True
                for r in range(size_r):
                    for c in range(size_c):
                        r_idx = (i + r) % len(rows)
                        c_idx = (j + c) % len(cols)
                        if kmap[(rows[r_idx], cols[c_idx])] != value:
                            valid = False
                            break
                        group.append((rows[r_idx], cols[c_idx]))
                    if not valid:
                        break
                if valid and group and not set(group).issubset(covered):
                    groups.append(group)
                    covered.update(group)

    return groups


def group_to_term(group, variables, num_vars, value=1):
    if not group:
        return None

    # Собираем все значения переменных в группе
    row_bits = set(row for row, _ in group)
    col_bits = set(col for _, col in group)

    term = []
    if num_vars == 1:
        bit = group[0][0]
        if (bit == '0' and value == 1) or (bit == '1' and value == 0):
            term.append(f"!{variables[0]}")
        else:
            term.append(variables[0])
    elif num_vars == 2:
        row_bit, col_bit = group[0][0], group[0][1]
        if len(row_bits) == 1:
            if (row_bit == '0' and value == 1) or (row_bit == '1' and value == 0):
                term.append(f"!{variables[0]}")
            else:
                term.append(variables[0])
        if len(col_bits) == 1:
            if (col_bit == '0' and value == 1) or (col_bit == '1' and value == 0):
                term.append(f"!{variables[1]}")
            else:
                term.append(variables[1])
    elif num_vars == 3:
        a_values = set(row for row, _ in group)
        b_values = set(col[0] for _, col in group)
        c_values = set(col[1] for _, col in group)

        if len(a_values) == 1:
            a_val = list(a_values)[0]
            if (a_val == '0' and value == 1) or (a_val == '1' and value == 0):
                term.append(f"!{variables[0]}")
            else:
                term.append(variables[0])
        if len(b_values) == 1:
            b_val = list(b_values)[0]
            if (b_val == '0' and value == 1) or (b_val == '1' and value == 0):
                term.append(f"!{variables[1]}")
            else:
                term.append(variables[1])
        if len(c_values) == 1:
            c_val = list(c_values)[0]
            if (c_val == '0' and value == 1) or (c_val == '1' and value == 0):
                term.append(f"!{variables[2]}")
            else:
                term.append(variables[2])
    elif num_vars == 4:
        a_values = set(row[0] for row, _ in group)
        b_values = set(row[1] for row, _ in group)
        c_values = set(col[0] for _, col in group)
        d_values = set(col[1] for _, col in group)

        if len(a_values) == 1:
            a_val = list(a_values)[0]
            if (a_val == '0' and value == 1) or (a_val == '1' and value == 0):
                term.append(f"!{variables[0]}")
            else:
                term.append(variables[0])
        if len(b_values) == 1:
            b_val = list(b_values)[0]
            if (b_val == '0' and value == 1) or (b_val == '1' and value == 0):
                term.append(f"!{variables[1]}")
            else:
                term.append(variables[1])
        if len(c_values) == 1:
            c_val = list(c_values)[0]
            if (c_val == '0' and value == 1) or (c_val == '1' and value == 0):
                term.append(f"!{variables[2]}")
            else:
                term.append(variables[2])
        if len(d_values) == 1:
            d_val = list(d_values)[0]
            if (d_val == '0' and value == 1) or (d_val == '1' and value == 0):
                term.append(f"!{variables[3]}")
            else:
                term.append(variables[3])
    else:  # num_vars == 5
        a_values = set(row[0] for row, _ in group)
        b_values = set(row[1] for row, _ in group)
        c_values = set(col[0] for _, col in group)
        d_values = set(col[1] for _, col in group)
        e_values = set(col[2] for _, col in group)

        if len(a_values) == 1:
            a_val = list(a_values)[0]
            if (a_val == '0' and value == 1) or (a_val == '1' and value == 0):
                term.append(f"!{variables[0]}")
            else:
                term.append(variables[0])
        if len(b_values) == 1:
            b_val = list(b_values)[0]
            if (b_val == '0' and value == 1) or (b_val == '1' and value == 0):
                term.append(f"!{variables[1]}")
            else:
                term.append(variables[1])
        if len(c_values) == 1:
            c_val = list(c_values)[0]
            if (c_val == '0' and value == 1) or (c_val == '1' and value == 0):
                term.append(f"!{variables[2]}")
            else:
                term.append(variables[2])
        if len(d_values) == 1:
            d_val = list(d_values)[0]
            if (d_val == '0' and value == 1) or (d_val == '1' and value == 0):
                term.append(f"!{variables[3]}")
            else:
                term.append(variables[3])
        if len(e_values) == 1:
            e_val = list(e_values)[0]
            if (e_val == '0' and value == 1) or (e_val == '1' and value == 0):
                term.append(f"!{variables[4]}")
            else:
                term.append(variables[4])

    return "&".join(term) if value == 1 else "|".join(term)


def minimize_sdnf_karnaugh(kmap_data, variables):
    print("\nМинимизация СДНФ методом карт Карно:")
    kmap, vars_, rows, cols = kmap_data
    print_karnaugh_map(kmap, variables, rows, cols)

    groups = find_groups(kmap, rows, cols, len(variables), value=1)
    if not groups:
        return "Не существует (функция всегда ложна)", []

    terms = []
    for group in groups:
        term = group_to_term(group, variables, len(variables), value=1)
        if term:
            terms.append(term)

    result = "|".join(f"({t})" for t in terms) if terms else "Пустое выражение"
    return result, terms


def minimize_sknf_karnaugh(kmap_data, variables):
    print("\nМинимизация СКНФ методом карт Карно:")
    kmap, vars_, rows, cols = kmap_data
    print_karnaugh_map(kmap, variables, rows, cols)

    groups = find_groups(kmap, rows, cols, len(variables), value=0)
    if not groups:
        return "Не существует (функция всегда истинна)", []

    terms = []
    for group in groups:
        term = group_to_term(group, variables, len(variables), value=0)
        if term:
            terms.append(term)

    result = "&".join(f"({t})" for t in terms) if terms else "Пустое выражение"
    return result, terms