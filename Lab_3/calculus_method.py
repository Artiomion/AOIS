def parse_term(term):
    term = term.replace('(', '').replace(')', '')
    literals = term.split('&' if '&' in term else '|')
    return [lit.replace('(!', '!').replace(')', '') for lit in literals]


def can_glue(term1, term2, op_type='&'):
    literals1 = parse_term(term1)
    literals2 = parse_term(term2)

    if len(literals1) != len(literals2):
        return False, None

    differences = 0
    glued_term = []
    diff_var = None

    for lit1, lit2 in zip(literals1, literals2):
        var1 = lit1.replace('!', '') if '!' in lit1 else lit1
        var2 = lit2.replace('!', '') if '!' in lit2 else lit2

        if var1 != var2:
            return False, None
        if lit1 != lit2:
            differences += 1
            diff_var = var1
        else:
            glued_term.append(lit1)

    if differences != 1:
        return False, None

    return True, op_type.join(glued_term)


def absorb(terms, op_type='&'):
    absorbed = []
    for i, term1 in enumerate(terms):
        keep = True
        literals1 = set(parse_term(term1))
        for j, term2 in enumerate(terms):
            if i != j:
                literals2 = set(parse_term(term2))
                if literals1.issubset(literals2) if op_type == '&' else literals2.issubset(literals1):
                    keep = False
                    break
        if keep:
            absorbed.append(term1)
    return absorbed


def minimize_calculus(terms, op_type='&'):
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

    if not current_terms:
        return "Пустое выражение", all_glued

    result = ('|' if op_type == '&' else '&').join([f"({t})" for t in current_terms])
    return result, all_glued


def minimize_sdnf_calculus(sdnf, variables):
    print("Минимизация СДНФ расчетным методом:")
    return minimize_calculus(sdnf, op_type='&')


def minimize_sknf_calculus(sknf, variables):
    print("Минимизация СКНФ расчетным методом:")
    return minimize_calculus(sknf, op_type='|')