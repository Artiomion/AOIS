class BinaryConverter:
    DEFAULT_BITS = 8
    CARRY_INITIAL = 1
    CARRY_RESET = 0
    BIT_SIGN_NEGATIVE = "1"

    def __init__(self, number, bits=DEFAULT_BITS):
        self.number = number
        self.bits = bits

    def convert_to_binary(self):
        if self.number >= 0:
            binary = ""
            for i in range(self.bits - 1, -1, -1):
                binary += "1" if (self.number & (1 << i)) else "0"
            return binary
        else:
            raise ValueError("Number must be positive")

    def show_binary(self):
        binary_number = self.convert_to_binary()
        print(f"Десятичное: {self.number}")
        print(f"Двоичное: {binary_number}")
        print(" ")

    def get_direct_code(self):
        sign = "0" if self.number >= 0 else "1"
        abs_value = abs(self.number)
        direct = BinaryConverter(abs_value, self.bits - 1).convert_to_binary()
        return f"{sign} {direct}"

    def show_direct_code(self):
        print(f"Десятичное: {self.number}")
        print(f"Прямой код: {self.get_direct_code()}")

    def get_reverse_code(self):
        if self.number >= 0:
            return self.get_direct_code()
        abs_value = abs(self.number)
        direct = BinaryConverter(abs_value, self.bits - 1).convert_to_binary()
        reverse = ''.join('1' if bit == '0' else '0' for bit in direct)
        return f"1 {reverse}"

    def show_reverse_code(self):
        print(f"Десятичное: {self.number}")
        print(f"Обратный код: {self.get_reverse_code()}")

    def get_additional_code(self):
        if self.number >= 0:
            direct = self.get_direct_code().split(" ")[1]
            return f"0 {direct.zfill(self.bits - 1)}"

        reverse = self.get_reverse_code().split(" ")[1]

        initial_carry = self.CARRY_INITIAL
        additional = ""
        for bit in reversed(reverse):
            if bit == "1" and initial_carry == 1:
                additional = "0" + additional
            elif bit == "0" and initial_carry == 1:
                additional = "1" + additional
                initial_carry = self.CARRY_RESET
            else:
                additional = bit + additional

        return f"{self.BIT_SIGN_NEGATIVE} {additional.zfill(self.bits - 1)}"

    def show_additional_code(self):
        print(f"Десятичное: {self.number}")
        print(f"Дополнительный код: {self.get_additional_code()}")

    def show_all_codes(self):
        print(f"Число введено: {self.number}")
        print(f"Прямой код: [{self.get_direct_code()}]")
        print(f"Обратный код: [{self.get_reverse_code()}]")
        print(f"Дополнительный код: [{self.get_additional_code()}]\n")

    def show_addition_result(self, result_decimal, result_additional, bits=8):
        converter = BinaryConverter(result_decimal, bits)
        print(f"Результат: {result_decimal}")
        print(f"Прямой код: [{converter.get_direct_code()}]")
        print(f"Обратный код: [{converter.get_reverse_code()}]")
        print(f"Дополнительный код: {result_additional}\n")

    def show_multiplication_result(self, result_decimal, result_direct, bits=8):
        converter = BinaryConverter(result_decimal, bits)
        print(f"Результат: {result_decimal}")
        print(f"Прямой код: {result_direct}")
        print(f"Обратный код: [{converter.get_reverse_code()}]")
        print(f"Дополнительный код: [{converter.get_additional_code()}]")


class ArithmeticOperations:
    DEFAULT_BITS = 8
    ERROR_OVERFLOW_MESSAGE = "Переполнение при сложении в дополнительном коде!"
    NEGATIVE_SIGN_ADJUSTMENT = 1
    BINARY_BASE = 2

    def __init__(self, number_1, number_2=None, bits=DEFAULT_BITS):
        self.number_1 = number_1
        self.number_2 = number_2
        self.bits = bits

    def add_in_additional_code(self):
        number_1_additional = ArithmeticOperations.get_additional_code(self.number_1, self.bits)
        number_2_additional = ArithmeticOperations.get_additional_code(self.number_2, self.bits)

        init_carry = 0
        result_additional = ""

        for i in range(self.bits - 1, -1, -1):
            bit1 = int(number_1_additional[i])
            bit2 = int(number_2_additional[i])

            sum_bit = bit1 + bit2 + init_carry
            result_additional = str(sum_bit % 2) + result_additional
            init_carry = sum_bit // 2

        sign_bit_1 = int(number_1_additional[0])
        sign_bit_2 = int(number_2_additional[0])
        sign_bit_res = int(result_additional[0])

        if (sign_bit_1 == sign_bit_2) and (sign_bit_res != sign_bit_1):
            raise OverflowError("Переполнение при сложении в дополнительном коде!")

        if result_additional[0] == "1":
            result_decimal = int(result_additional, ArithmeticOperations.BINARY_BASE) - (ArithmeticOperations.NEGATIVE_SIGN_ADJUSTMENT << self.bits)
        else:
            result_decimal = int(result_additional, ArithmeticOperations.BINARY_BASE)

        return result_decimal, result_additional

    def subtract_in_additional_code(self):
        self.number_2 = -self.number_2
        return self.add_in_additional_code()

    def show_addition_result(self, result_decimal, result_additional):
        print(f"Результат: {result_decimal}")
        converter_result = BinaryConverter(result_decimal, self.bits)
        print(f"Прямой код: [{converter_result.get_direct_code()}]")
        print(f"Обратный код: [{converter_result.get_reverse_code()}]")
        print(f"Дополнительный код: {result_additional}\n")

    def show_number_info(self, number):
        converter = BinaryConverter(number, self.bits)
        print(f"Число введено: {number}")
        print(f"Прямой код: [{converter.get_direct_code()}]")
        print(f"Обратный код: [{converter.get_reverse_code()}]")
        print(f"Дополнительный код: [{converter.get_additional_code()}]\n")

    @staticmethod
    def get_additional_code(number, bits):
        if number >= 0:
            bin_number = bin(number)[2:].zfill(bits)
        else:
            bin_number = bin((ArithmeticOperations.NEGATIVE_SIGN_ADJUSTMENT << bits) + number)[ArithmeticOperations.NEGATIVE_SIGN_ADJUSTMENT:]
        return bin_number[-bits:]


class BinaryOperations:
    DEFAULT_BITS = 8
    DEFAULT_PRECISION = 5
    DIRECT_CODE_TAG = "Прямой код"

    def __init__(self, number_1, number_2=None, bits=DEFAULT_BITS):
        self.number_1 = number_1
        self.number_2 = number_2
        self.bits = bits

    def multiply_in_direct_code(self):
        number_1_direct = self.get_direct_code(self.number_1)
        number_2_direct = self.get_direct_code(self.number_2)

        sign_1 = int(number_1_direct[0])
        sign_2 = int(number_2_direct[0])

        number_1_abs = int(number_1_direct[1:], 2)
        number_2_abs = int(number_2_direct[1:], 2)

        result_abs = number_1_abs * number_2_abs

        result_sign = "0" if sign_1 == sign_2 else "1"

        max_value = (1 << (self.bits - 1)) - 1
        if result_abs > max_value:
            OVERFLOW_ERROR = "Переполнение: результат {result_abs} не помещается в {self.bits} бит."
            raise OverflowError(OVERFLOW_ERROR)

        result_binary = bin(result_abs)[2:].zfill(self.bits - 1)
        result_binary = result_sign + result_binary

        result_decimal = -result_abs if result_sign == "1" else result_abs

        return result_decimal, result_binary

    def divide_with_precision(self, precision=DEFAULT_PRECISION):
        if self.number_2 == 0:
            DIVISION_BY_ZERO_ERROR = "Деление на ноль невозможно!"
            raise ZeroDivisionError(DIVISION_BY_ZERO_ERROR)

        def direct_code(n):
            if n >= 0:
                return f"0{n:0{self.bits - 1}b}"
            else:
                return f"1{(-n):0{self.bits - 1}b}"

        number_1_direct = direct_code(self.number_1)
        number_2_direct = direct_code(self.number_2)

        sign_1 = int(number_1_direct[0])
        sign_2 = int(number_2_direct[0])
        result_sign = "0" if sign_1 == sign_2 else "1"

        dividend = int(number_1_direct[1:], 2)
        divisor = int(number_2_direct[1:], 2)

        shift_count = 0
        while divisor < dividend:
            divisor <<= 1
            shift_count += 1

        quotient = ""

        for _ in range(shift_count + 1):
            if dividend >= divisor:
                quotient += "1"
                dividend -= divisor
            else:
                quotient += "0"
            divisor >>= 1

        BINARY_POINT = "."
        quotient += BINARY_POINT

        for _ in range(precision):
            dividend <<= 1
            if dividend >= int(number_2_direct[1:], 2):
                quotient += "1"
                dividend -= int(number_2_direct[1:], 2)
            else:
                quotient += "0"

        integer_part, fractional_part = quotient.split(".")
        decimal_value = int(integer_part, 2) + sum(
            int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(fractional_part)
        )

        if result_sign == "1":
            decimal_value = -decimal_value

        res_binary = result_sign + integer_part + "." + fractional_part

        return decimal_value, res_binary

    def show_multiplication_result(self, decimal_value, res_binary, bits=DEFAULT_BITS):
        converter = BinaryConverter(decimal_value, bits)
        print(f"Результат: {decimal_value}")
        print(f"Прямой код: {res_binary}")
        print(f"Обратный код: [{converter.get_reverse_code()}]")
        print(f"Дополнительный код: [{converter.get_additional_code()}]")

    def show_number_info(self, number, bits=DEFAULT_BITS):
        converter = BinaryConverter(number, self.bits)
        print(f"Число введено: {number}")
        print(f"Прямой код: [{converter.get_direct_code()}]")
        print(f"Обратный код: [{converter.get_reverse_code()}]")
        print(f"Дополнительный код: [{converter.get_additional_code()}]\n")

    def get_direct_code(self, number):
        if number >= 0:
            bin_number = bin(number)[2:].zfill(self.bits - 1)
            return "0" + bin_number
        else:
            bin_number = bin(abs(number))[2:].zfill(self.bits - 1)
            return "1" + bin_number


class FloatingPointIEEE754:
    EXPONENT_BIAS = 127
    IEEE754_TOTAL_BITS = 32
    IEEE754_MAX_EXPONENT = 255
    IEEE754_MANTISSA_BITS = 23
    IEEE754_EXPONENT_BITS = 8

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def float_to_ieee754(self, num):
        sign = '1' if num < 0 else '0'
        if num == 0:
            return '0' * self.IEEE754_TOTAL_BITS

        num = abs(num)
        int_part = int(num)
        frac_part = num - int_part
        int_bin = bin(int_part)[2:] if int_part > 0 else ''
        frac_bin = ''

        while frac_part and len(frac_bin) < self.IEEE754_MANTISSA_BITS:
            frac_part *= 2
            bit = int(frac_part)
            frac_bin += str(bit)
            frac_part -= bit

        if int_bin:
            exp = len(int_bin) - 1
        elif '1' in frac_bin:
            exp = -frac_bin.index('1') - 1
        else:
            return '0' * self.IEEE754_TOTAL_BITS

        exp_bits = bin(exp + self.EXPONENT_BIAS)[2:].zfill(self.IEEE754_EXPONENT_BITS)
        mantissa_bits = (int_bin[1:] + frac_bin).ljust(self.IEEE754_MANTISSA_BITS, '0')[:self.IEEE754_MANTISSA_BITS]

        return f'{sign}{exp_bits}{mantissa_bits}'

    def ieee754_to_float(self, ieee_bin):
        sign = int(ieee_bin[0])
        exp = int(ieee_bin[1:9], 2) - self.EXPONENT_BIAS
        mantissa = ieee_bin[9:]

        if exp == -127:
            mantissa_value = 0.0
            for i, bit in enumerate(mantissa):
                if bit == '1':
                    mantissa_value += 2 ** -(i + 1)
            result = mantissa_value * (2 ** -(self.EXPONENT_BIAS - 1))
        else:
            mantissa_value = 1.0
            for i, bit in enumerate(mantissa):
                if bit == '1':
                    mantissa_value += 2 ** -(i + 1)
            result = mantissa_value * (2 ** exp)

        return -result if sign else result

    def add_ieee754_numbers(self):
        a_ieee = self.float_to_ieee754(self.num1)
        b_ieee = self.float_to_ieee754(self.num2)

        sign_a, exp_a, mant_a = int(a_ieee[0]), int(a_ieee[1:9], 2), int('1' + a_ieee[self.IEEE754_EXPONENT_BITS + 1:],
                                                                         2)
        sign_b, exp_b, mant_b = int(b_ieee[0]), int(b_ieee[1:9], 2), int('1' + b_ieee[self.IEEE754_EXPONENT_BITS:], 2)

        if exp_a > exp_b:
            shift = exp_a - exp_b
            mant_b >>= shift
            exp_b = exp_a
        elif exp_b > exp_a:
            shift = exp_b - exp_a
            mant_a >>= shift
            exp_a = exp_b

        if sign_a:
            mant_a = -mant_a
        if sign_b:
            mant_b = -mant_b

        mant_sum = mant_a + mant_b
        sign_res = 0 if mant_sum >= 0 else 1
        mant_sum = abs(mant_sum)
        exp_res = exp_a

        if mant_sum == 0:
            return '0' * self.IEEE754_TOTAL_BITS

        while mant_sum and not (mant_sum & (1 << self.IEEE754_MANTISSA_BITS)):
            mant_sum <<= 1
            exp_res -= 1

        if mant_sum & (1 << (self.IEEE754_MANTISSA_BITS + 1)):
            mant_sum >>= 1
            exp_res += 1

        if exp_res <= 0:
            exp_res = 0
            mant_sum = 0
        elif exp_res >= self.IEEE754_MAX_EXPONENT:
            exp_res = self.IEEE754_MAX_EXPONENT
            mant_sum = 0

        mantissa_bits = bin(mant_sum)[3:3 + self.IEEE754_MANTISSA_BITS].ljust(self.IEEE754_MANTISSA_BITS, '0')
        exp_bits = bin(exp_res)[2:].zfill(self.IEEE754_EXPONENT_BITS)

        return f'{sign_res}{exp_bits}{mantissa_bits}'

    def get_ieee754_sum(self):
        num1 = self.float_to_ieee754(self.num1)
        num2 = self.float_to_ieee754(self.num2)
        return self.add_ieee754_numbers()