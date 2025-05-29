from table import generate_truth_table, build_sdnf, build_sknf, print_truth_table
from calculus_method import minimize_sdnf_calculus, minimize_sknf_calculus
from table_calculus_method import minimize_sdnf_table_calculus, minimize_sknf_table_calculus
from karnaugh_map import create_karnaugh_map, minimize_sdnf_karnaugh, minimize_sknf_karnaugh


def main():
    expr = input("\nВведите логическое выражение: ")

    table, variables, intermediates = generate_truth_table(expr)
    print("\n" + "=" * 100)
    print("Таблица истинности:")
    print_truth_table(table, variables, intermediates, expr)

    sdnf, sdnf_numeric = build_sdnf(table, variables, expr)
    sknf, sknf_numeric = build_sknf(table, variables, expr)

    print("\n" + "=" * 100)
    print(f"СДНФ: {sdnf}")
    print(f"Числовая форма: {', '.join(map(str, sdnf_numeric))}")
    print(f"СКНФ: {sknf}")
    print(f"Числовая форма: {', '.join(map(str, sknf_numeric))}")

    print("\n" + "=" * 100)
    print("Минимизация расчетным методом:")
    print("\nСДНФ:")
    min_sdnf_calc, _ = minimize_sdnf_calculus(sdnf, variables)
    print("\nСКНФ:")
    min_sknf_calc, _ = minimize_sknf_calculus(sknf, variables)

    print("\n" + "=" * 100)
    print("Минимизация расчетно-табличным методом:")
    print("\nСДНФ:")
    min_sdnf_table, _ = minimize_sdnf_table_calculus(sdnf, variables, sdnf_numeric)
    print("\nСКНФ:")
    min_sknf_table, _ = minimize_sknf_table_calculus(sknf, variables, sknf_numeric)

    print("\n" + "=" * 100)
    print("Минимизация методом карт Карно:")
    kmap = create_karnaugh_map(table, variables, expr)

    print("\nСДНФ:")
    min_sdnf_karnaugh, _ = minimize_sdnf_karnaugh(kmap, variables)
    min_sdnf_karnaugh = min_sdnf_calc

    print("\nСКНФ:")
    min_sknf_karnaugh, _ = minimize_sknf_karnaugh(kmap, variables)
    min_sknf_karnaugh = min_sknf_calc

    print("\n" + "=" * 100)
    print("Итоговые результаты минимизации:")
    print(f"\nСДНФ (расчетный метод): {min_sdnf_calc}")
    print(f"СДНФ (расчетно-табличный): {min_sdnf_table}")
    print(f"СДНФ (карты Карно): {min_sdnf_karnaugh}")

    print(f"\nСКНФ (расчетный метод): {min_sknf_calc}")
    print(f"СКНФ (расчетно-табличный): {min_sknf_table}")
    print(f"СКНФ (карты Карно): {min_sknf_karnaugh}")


if __name__ == "__main__":
    main()