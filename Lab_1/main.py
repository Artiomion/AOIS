from binary_operations import BinaryConverter, ArithmeticOperations, BinaryOperations, FloatingPointIEEE754

class Application:
    def __init__(self):
        self.actions = {
            1: self.convert_to_binary,
            2: self.convert_to_direct,
            3: self.convert_to_reverse,
            4: self.convert_to_additional,
            5: self.add_numbers,
            6: self.subtract_numbers,
            7: self.multiply_numbers,
            8: self.divide_numbers,
            9: self.add_floating_point,
            10: self.exit_program
        }

    def show_menu(self):
        print("\nВыберите действие:")
        print("1. Перевести в двоичную систему счисления")
        print("2. Перевести в двоичную систему в прямом коде")
        print("3. Перевести в двоичную систему в обратном коде")
        print("4. Перевести в двоичную систему в дополнительном коде")
        print("5. Найти сумму в дополнительном коде")
        print("6. Найти разность в дополнительном коде")
        print("7. Умножить в прямом коде")
        print("8. Разделить с точностью до 5 знаков")
        print("9. Найти сумму 2 положительных чисел с плавающей точкой по IEEE-754-2008")
        print("10. Завершить")

    def get_integer_input(self, prompt, default=None):
        while True:
            try:
                value = input(prompt)
                if default and not value:
                    return default
                return int(value)
            except ValueError:
                print("Ошибка: введите целое число.")

    def get_float_input(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Ошибка: введите число.")

    def convert_to_binary(self):
        number = self.get_integer_input("Введите число: ")
        bits = self.get_integer_input("Введите разрядность: ")
        converter = BinaryConverter(number, bits)
        converter.show_binary()

    def convert_to_direct(self):
        number = self.get_integer_input("Введите число: ")
        bits = self.get_integer_input("Введите разрядность: ")
        converter = BinaryConverter(number, bits)
        converter.show_direct_code()

    def convert_to_reverse(self):
        number = self.get_integer_input("Введите число: ")
        bits = self.get_integer_input("Введите разрядность: ")
        converter = BinaryConverter(number, bits)
        converter.show_reverse_code()

    def convert_to_additional(self):
        number = self.get_integer_input("Введите число: ")
        bits = self.get_integer_input("Введите разрядность: ")
        converter = BinaryConverter(number, bits)
        converter.show_additional_code()

    def add_numbers(self):
        print("\nСложение:")
        number1 = self.get_integer_input("Введите число №1: ")
        number2 = self.get_integer_input("Введите число №2: ")
        bits = self.get_integer_input("Введите разрядность (по умолчанию 8): ", 8)

        operations = ArithmeticOperations(number1, number2, bits)
        self.show_number_info(operations, number1, "Число 1:")
        self.show_number_info(operations, number2, "Число 2:")

        result_decimal, result_additional = operations.add_in_additional_code()
        operations.show_addition_result(result_decimal, result_additional)

    def subtract_numbers(self):
        print("\nВычитание:")
        number1 = self.get_integer_input("Введите число №1: ")
        number2 = self.get_integer_input("Введите число №2: ")
        bits = self.get_integer_input("Введите разрядность (по умолчанию 8): ", 8)

        operations = ArithmeticOperations(number1, number2, bits)
        self.show_number_info(operations, number1, "Число 1:")
        self.show_number_info(operations, number2, "Число 2:")

        result_decimal, result_additional = operations.subtract_in_additional_code()
        operations.show_addition_result(result_decimal, result_additional)

    def multiply_numbers(self):
        print("\nУмножение:")
        number1 = self.get_integer_input("Введите число №1: ")
        number2 = self.get_integer_input("Введите число №2: ")
        bits = self.get_integer_input("Введите разрядность (по умолчанию 8): ", 8)

        operations = BinaryOperations(number1, number2, bits)
        self.show_number_info(operations, number1, "Число 1:")
        self.show_number_info(operations, number2, "Число 2:")

        result_decimal, result_additional = operations.multiply_in_direct_code()
        operations.show_multiplication_result(result_decimal, result_additional)

    def divide_numbers(self):
        print("\nДеление:")
        number1 = self.get_integer_input("Введите число №1: ")
        number2 = self.get_integer_input("Введите число №2: ")
        bits = self.get_integer_input("Введите разрядность (по умолчанию 8): ", 8)

        operations = BinaryOperations(number1, number2, bits)
        self.show_number_info(operations, number1, "Число 1:")
        self.show_number_info(operations, number2, "Число 2:")

        result_decimal, result_additional = operations.divide_with_precision()
        print(f"\nРезультат деления в десятичном виде: {result_decimal}")
        print(f"Результат деления в прямом коде: {result_additional}")

    def add_floating_point(self):
        print("\nСложение чисел с плавающей точкой:")
        number1 = self.get_float_input("Введите число №1: ")
        number2 = self.get_float_input("Введите число №2: ")

        standard = FloatingPointIEEE754(number1, number2)
        ieee_number1 = standard.float_to_ieee754(number1)
        ieee_number2 = standard.float_to_ieee754(number2)

        ieee_result = standard.add_ieee754_numbers()
        result_float = standard.ieee754_to_float(ieee_result)

        print(f"\nЧисло A ({number1}) -> IEEE-754: {ieee_number1}")
        print(f"Число B ({number2}) -> IEEE-754: {ieee_number2}")
        print(f"Сумма в IEEE-754 формате: {ieee_result}")
        print(f"Сумма в десятичном формате: {result_float}")

    def show_number_info(self, converter, number, label):
        print(f"\n{label}")
        converter.show_number_info(number)

    def exit_program(self):
        print("\nВыход из программы.")
        return False

    def run(self):
        try:
            running = True
            while running:
                self.show_menu()
                try:
                    choice = self.get_integer_input("Выберите действие: ")
                    action = self.actions.get(choice)
                    if action:
                        running = action() is not False
                    else:
                        print("Неверный выбор. Попробуйте снова.")
                except Exception as e:
                    print(f"Произошла ошибка: {str(e)}")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем.")
        finally:
            print("Программа завершена.")


if __name__ == '__main__':
    app = Application()
    app.run()