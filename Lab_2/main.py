from table import calculate_index_form, build_sknf, build_sdnf, print_truth_table, generate_truth_table


def main():
    print("Введите формулу:", end=" ")
    expr = input().strip()

    try:
        table, variables, intermediates = generate_truth_table(expr)
    except Exception as e:
        print("Ошибка в выражении:", e)
        return

    # Выводим таблицу истинности
    print_truth_table(table, variables, intermediates, expr)

    # Строим и выводим СДНФ
    sdnf, sdnf_numeric = build_sdnf(table, variables, expr)
    print("\nСДНФ:")
    print(sdnf)

    # Строим и выводим СКНФ
    sknf, sknf_numeric = build_sknf(table, variables, expr)
    print("\nСКНФ:")
    print(sknf)

    # Выводим числовую форму
    print("\nЧисловая форма:")
    print(f"СДНФ: ({' '.join(map(str, sdnf_numeric))}) |")
    print(f"СКНФ: ({' '.join(map(str, sknf_numeric))}) &")

    # Выводим индексную форму
    index = calculate_index_form(table, expr)
    print("\nИндексная форма:")
    print(f"Десятичная: {index}")
    print(f"Двоичная: {bin(index)[2:].zfill(len(table))}")


if __name__ == "__main__":
    main()