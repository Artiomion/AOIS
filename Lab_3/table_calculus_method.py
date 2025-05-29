import itertools
from calculus_method import parse_term, can_glue, absorb

def build_implication_table(terms, numeric_form, variables, op_type='&'):
    parsed_terms = [parse_term(term) for term in terms]

    coverage_table = {term: [] for term in terms}
    for term_idx, term in enumerate(terms):
        term_literals = parsed_terms[term_idx]
        for idx in numeric_form:
            row = format(idx, f'0{len(variables)}b')
            match = False if op_type == '|' else True
            for lit in term_literals:
                var = lit.replace('!', '') if '!' in lit else lit
                if var not in variables:
                    match = False
                    break
                var_idx = variables.index(var)
                var_value = int(row[var_idx])
                if op_type == '&':
                    if '!' in lit and var_value == 1:
                        match = False
                    elif lit == var and var_value == 0:
                        match = False
                else:
                    if '!' in lit and var_value == 0:
                        match = True
                    elif lit == var and var_value == 1:
                        match = True
            if match:
                coverage_table[term].append(idx)


    essential_terms = []
    covered = set()
    remaining_minterms = set(numeric_form)


    for term in terms:
        unique_coverage = set(coverage_table[term]) - covered
        if unique_coverage & remaining_minterms:
            essential_terms.append(term)
            covered.update(coverage_table[term])


    while remaining_minterms - covered:
        best_term = None
        max_coverage = 0
        for term in terms:
            if term not in essential_terms:
                new_coverage = len(set(coverage_table[term]) & (remaining_minterms - covered))
                if new_coverage > max_coverage:
                    max_coverage = new_coverage
                    best_term = term
        if best_term:
            essential_terms.append(best_term)
            covered.update(coverage_table[best_term])
        else:
            break


    print("\nТаблица покрытия:")
    literals = [var for var in variables] + [f"!{var}" for var in variables]
    max_literal_len = max(len(lit) for lit in literals)
    max_term_len = max(len(term) for term in terms)
    header = "Переменные".ljust(max_literal_len) + " | " + " | ".join(
        f"{i:2} ({format(i, f'0{len(variables)}b')})".center(max_term_len + 8) for i in numeric_form)
    print(header)
    print("-" * len(header))

    for var in variables:
        row = var.ljust(max_literal_len) + " | "
        row += " | ".join(
            str(int(format(i, f'0{len(variables)}b')[variables.index(var)])).center(max_term_len + 8) for i in numeric_form)
        print(row)
    for var in variables:
        row = f"!{var}".ljust(max_literal_len) + " | "
        row += " | ".join(
            str(1 - int(format(i, f'0{len(variables)}b')[variables.index(var)])).center(max_term_len + 8) for i in numeric_form)
        print(row)

    print("\nПокрытие термов:")
    for term in terms:
        row = term.ljust(max_literal_len) + " | "
        row += " | ".join(
            "O".center(max_term_len + 8) if i in coverage_table[term] else "x".center(max_term_len + 8) for i in numeric_form)
        print(row)


    result = ('|' if op_type == '&' else '&').join(f"({t})" for t in essential_terms)
    return result, essential_terms

def minimize_table_calculus(terms, numeric_form, variables, op_type='&'):
    if not terms or terms in ["Не существует (функция всегда ложна)", "Не существует (функция всегда истинна)"]:
        return terms, []

    current_terms = terms.split('|' if op_type == '&' else '&')
    current_terms = [t.strip('() ').replace('(!', '!').replace(')', '') for t in current_terms]
    stage = 1
    all_glued = []
    print(f"\nНачальные термы: {', '.join(current_terms)}")

    while True:
        glued_terms = []
        used = set()
        new_terms = []

        for i, term1 in enumerate(current_terms):
            for j, term2 in enumerate(current_terms[i + 1:], start=i + 1):
                can, result = can_glue(term1, term2, op_type)
                if can and result not in glued_terms:
                    glued_terms.append(result)
                    used.add(term1)
                    used.add(term2)

        for term in current_terms:
            if term not in used:
                new_terms.append(term)

        new_terms.extend(glued_terms)

        new_terms = absorb(new_terms, op_type)

        if not glued_terms:
            break

        all_glued.extend(glued_terms)
        print(f"\nСтадия {stage} склеивания:")
        for glued in glued_terms:
            print(f"  {glued}")
        print(f"Термы после стадии {stage}: {', '.join(new_terms)}")
        current_terms = new_terms
        stage += 1

    result, essential_terms = build_implication_table(current_terms, numeric_form, variables, op_type)
    return result, all_glued + essential_terms

def minimize_sdnf_table_calculus(sdnf, variables, numeric_form):
    print("Минимизация СДНФ расчетно-табличным методом:")
    return minimize_table_calculus(sdnf, numeric_form, variables, op_type='&')

def minimize_sknf_table_calculus(sknf, variables, numeric_form):
    print("Минимизация СКНФ расчетно-табличным методом:")
    return minimize_table_calculus(sknf, numeric_form, variables, op_type='|')