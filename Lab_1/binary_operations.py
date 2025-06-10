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
        def determine_output_sign(a, b):
            return (a < 0) != (b < 0)

        def calculate_absolute(n):
            return n if n >= 0 else -n

        def check_overflow_boundary(x, y, bit_size):
            threshold = (1 << (bit_size - 1)) - 1
            return y > 0 and x > threshold // y

        def binary_product(x, y, max_bits):
            total = 0
            current_value = x
            remaining_ops = y

            while remaining_ops:
                if remaining_ops % 2:
                    total += current_value
                current_value *= 2
                remaining_ops //= 2

                if total > max_bits:
                    raise OverflowError(f"Превышение лимита {max_bits}")
            return total

        abs_first = calculate_absolute(self.number_1)
        abs_second = calculate_absolute(self.number_2)
        is_negative = determine_output_sign(self.number_1, self.number_2)

        max_allowed = (1 << (self.bits - 1)) - 1

        if check_overflow_boundary(abs_first, abs_second, max_allowed):
            raise ArithmeticError(f"Потенциальное переполнение {self.bits - 1} бит")

        product_value = binary_product(abs_first, abs_second, max_allowed)

        def format_binary_output(value, sign_flag, total_bits):
            magnitude_bits = bin(value)[2:].zfill(total_bits - 1)
            return ('1' if sign_flag else '0') + magnitude_bits

        binary_output = format_binary_output(product_value, is_negative, self.bits)
        decimal_result = -product_value if is_negative else product_value

        return (decimal_result, binary_output)


    #######################
    def divide_with_precision(self, fractional_bits=5):
        class NumberSign:
            def __init__(self, val):
                self.is_non_negative = val >= 0
                self.magnitude = abs(val)

        if not self.number_2:
            raise ZeroDivisionError("Деление на ноль запрещено")

        dividend = NumberSign(self.number_1)
        divisor = NumberSign(self.number_2)
        result_positive = dividend.is_non_negative == divisor.is_non_negative

        def calculate_integer_part(a, b):
            count = 0
            while a >= b:
                a -= b
                count += 1
            return count, a

        int_part, remaining = calculate_integer_part(
            dividend.magnitude,
            divisor.magnitude
        )

        def compute_fraction(diff, denom, precision):
            bits = []
            for _ in range(precision):
                diff <<= 1
                if diff >= denom:
                    bits.append(1)
                    diff -= denom
                else:
                    bits.append(0)
            return bits, diff

        fraction_bits, final_remainder = compute_fraction(
            remaining,
            divisor.magnitude,
            fractional_bits
        )

        def to_binary_string(integer, fraction):
            return f"{bin(integer)[2:]}.{''.join(map(str, fraction))}"

        binary_representation = to_binary_string(int_part, fraction_bits)

        def convert_to_decimal(whole, bits, sign):
            decimal = whole
            for i, bit in enumerate(bits, 1):
                decimal += bit * (0.5 ** i)
            return decimal if sign else -decimal

        decimal_value = convert_to_decimal(
            int_part,
            fraction_bits,
            result_positive
        )

        def format_signed_binary(sign, binary_str):
            return f"{int(not sign)} {binary_str}"

        signed_binary = format_signed_binary(
            result_positive,
            binary_representation
        )

        return (decimal_value, signed_binary)

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
        if num == 0:
            return '0' * self.IEEE754_TOTAL_BITS

        sign = '1' if num < 0 else '0'
        num = abs(num)

        if num == float('inf'):
            return sign + '1' * self.IEEE754_EXPONENT_BITS + '0' * self.IEEE754_MANTISSA_BITS
        if num != num:
            return sign + '1' * self.IEEE754_EXPONENT_BITS + '1' * self.IEEE754_MANTISSA_BITS

        exponent = 0
        if num >= 1.0:
            while num >= 2.0:
                num /= 2.0
                exponent += 1
        else:
            while num < 1.0:
                num *= 2.0
                exponent -= 1

        mantissa = num - 1.0
        mantissa_bits = ''
        for _ in range(self.IEEE754_MANTISSA_BITS):
            mantissa *= 2
            bit = int(mantissa)
            mantissa_bits += str(bit)
            mantissa -= bit

        if mantissa >= 0.5:
            mantissa_bits = bin(int(mantissa_bits, 2) + 1)[2:].zfill(self.IEEE754_MANTISSA_BITS)

        exponent += self.EXPONENT_BIAS
        if exponent <= 0:
            return sign + '0' * self.IEEE754_EXPONENT_BITS + mantissa_bits
        if exponent >= self.IEEE754_MAX_EXPONENT:
            return sign + '1' * self.IEEE754_EXPONENT_BITS + '0' * self.IEEE754_MANTISSA_BITS

        exponent_bits = bin(exponent)[2:].zfill(self.IEEE754_EXPONENT_BITS)
        return sign + exponent_bits + mantissa_bits

    def ieee754_to_float(self, ieee_bin):
        if len(ieee_bin) != self.IEEE754_TOTAL_BITS:
            raise ValueError("Недопустимая длина двоичной строки IEEE-754")

        sign = -1 if ieee_bin[0] == '1' else 1
        exponent = int(ieee_bin[1:9], 2)
        mantissa_bits = ieee_bin[9:]

        if exponent == self.IEEE754_MAX_EXPONENT:
            if mantissa_bits == '0' * self.IEEE754_MANTISSA_BITS:
                return sign * float('inf')
            else:
                return float('nan')

        if exponent == 0:
            mantissa = int(mantissa_bits, 2) / (2 ** self.IEEE754_MANTISSA_BITS)
            return sign * mantissa * (2 ** (-126))
        else:
            mantissa = 1 + int(mantissa_bits, 2) / (2 ** self.IEEE754_MANTISSA_BITS)
            return sign * mantissa * (2 ** (exponent - self.EXPONENT_BIAS))

    def add_ieee754_numbers(self):
        def decompose(ieee):
            sign = int(ieee[0])
            exponent = int(ieee[1:9], 2)
            mantissa = int(ieee[9:], 2)
            return sign, exponent, mantissa

        def compose(sign, exponent, mantissa):
            exponent_bits = bin(exponent)[2:].zfill(self.IEEE754_EXPONENT_BITS)
            mantissa_bits = bin(mantissa)[2:].zfill(self.IEEE754_MANTISSA_BITS)
            return f"{sign}{exponent_bits}{mantissa_bits}"

        a_ieee = self.float_to_ieee754(self.num1)
        b_ieee = self.float_to_ieee754(self.num2)

        sign_a, exp_a, mant_a = decompose(a_ieee)
        sign_b, exp_b, mant_b = decompose(b_ieee)


        if exp_a == self.IEEE754_MAX_EXPONENT or exp_b == self.IEEE754_MAX_EXPONENT:
            return compose(0, self.IEEE754_MAX_EXPONENT, 0)

        if exp_a != 0:
            mant_a |= 1 << self.IEEE754_MANTISSA_BITS
        if exp_b != 0:
            mant_b |= 1 << self.IEEE754_MANTISSA_BITS

        shift = abs(exp_a - exp_b)
        if exp_a > exp_b:
            mant_b >>= shift
            exp_res = exp_a
        else:
            mant_a >>= shift
            exp_res = exp_b

        if sign_a:
            mant_a = -mant_a
        if sign_b:
            mant_b = -mant_b

        mant_sum = mant_a + mant_b

        sign_res = 0 if mant_sum >= 0 else 1
        mant_sum = abs(mant_sum)

        if mant_sum == 0:
            return compose(0, 0, 0)

        leading_pos = mant_sum.bit_length() - 1
        if leading_pos > self.IEEE754_MANTISSA_BITS:
            shift = leading_pos - self.IEEE754_MANTISSA_BITS
            mant_sum >>= shift
            exp_res += shift
        elif leading_pos < self.IEEE754_MANTISSA_BITS:
            shift = self.IEEE754_MANTISSA_BITS - leading_pos
            mant_sum <<= shift
            exp_res -= shift

        mant_sum &= (1 << self.IEEE754_MANTISSA_BITS) - 1

        if exp_res >= self.IEEE754_MAX_EXPONENT:
            return compose(sign_res, self.IEEE754_MAX_EXPONENT, 0)
        elif exp_res <= 0:
            return compose(sign_res, 0, mant_sum)

        return compose(sign_res, exp_res, mant_sum)

    def get_ieee754_sum(self):
        return self.add_ieee754_numbers()