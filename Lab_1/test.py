import unittest
from binary_operations import BinaryConverter, ArithmeticOperations, BinaryOperations, FloatingPointIEEE754


class TestBinaryConverter(unittest.TestCase):
    def setUp(self):
        self.positive_num = 5
        self.negative_num = -5
        self.bits = 8

    def test_convert_to_binary_positive(self):
        converter = BinaryConverter(self.positive_num, self.bits)
        self.assertEqual(converter.convert_to_binary(), "00000101")

    def test_convert_to_binary_negative_raises(self):
        converter = BinaryConverter(self.negative_num, self.bits)
        with self.assertRaises(ValueError):
            converter.convert_to_binary()

    def test_get_direct_code_positive(self):
        converter = BinaryConverter(self.positive_num, self.bits)
        self.assertEqual(converter.get_direct_code(), "0 0000101")

    def test_get_direct_code_negative(self):
        converter = BinaryConverter(self.negative_num, self.bits)
        self.assertEqual(converter.get_direct_code(), "1 0000101")

    def test_get_reverse_code_positive(self):
        converter = BinaryConverter(self.positive_num, self.bits)
        self.assertEqual(converter.get_reverse_code(), "0 0000101")

    def test_get_reverse_code_negative(self):
        converter = BinaryConverter(self.negative_num, self.bits)
        self.assertEqual(converter.get_reverse_code(), "1 1111010")

    def test_get_additional_code_positive(self):
        converter = BinaryConverter(self.positive_num, self.bits)
        self.assertEqual(converter.get_additional_code(), "0 0000101")

    def test_get_additional_code_negative(self):
        converter = BinaryConverter(self.negative_num, self.bits)
        self.assertEqual(converter.get_additional_code(), "1 1111011")

    def test_show_methods(self):
        converter = BinaryConverter(self.positive_num, self.bits)
        converter.show_binary()
        converter.show_direct_code()
        converter.show_reverse_code()
        converter.show_additional_code()
        converter.show_all_codes()

    def test_show_addition_result(self):
        converter = BinaryConverter(10, self.bits)
        converter.show_addition_result(15, "00001111")

    def test_show_multiplication_result(self):
        converter = BinaryConverter(10, self.bits)
        converter.show_multiplication_result(15, "00001111")


class TestArithmeticOperations(unittest.TestCase):
    def setUp(self):
        self.num1 = 5
        self.num2 = 3
        self.bits = 8

    def test_add_in_additional_code_positive(self):
        ops = ArithmeticOperations(self.num1, self.num2, self.bits)
        result_decimal, result_additional = ops.add_in_additional_code()
        self.assertEqual(result_decimal, 8)
        self.assertEqual(result_additional, "00001000")

    def test_add_in_additional_code_negative(self):
        ops = ArithmeticOperations(-self.num1, -self.num2, self.bits)
        result_decimal, result_additional = ops.add_in_additional_code()
        self.assertEqual(result_decimal, -8)
        self.assertEqual(result_additional, "11111000")

    def test_add_in_additional_code_mixed(self):
        ops = ArithmeticOperations(self.num1, -self.num2, self.bits)
        result_decimal, result_additional = ops.add_in_additional_code()
        self.assertEqual(result_decimal, 2)
        self.assertEqual(result_additional, "00000010")

    def test_add_in_additional_code_overflow(self):
        ops = ArithmeticOperations(127, 1, 8)
        with self.assertRaises(OverflowError):
            ops.add_in_additional_code()

    def test_subtract_in_additional_code(self):
        ops = ArithmeticOperations(self.num1, self.num2, self.bits)
        result_decimal, result_additional = ops.subtract_in_additional_code()
        self.assertEqual(result_decimal, 2)
        self.assertEqual(result_additional, "00000010")

    def test_get_additional_code_static(self):
        self.assertEqual(ArithmeticOperations.get_additional_code(5, 8), "00000101")
        self.assertEqual(ArithmeticOperations.get_additional_code(-5, 8), "11111011")

    def test_show_addition_result(self):
        ops = ArithmeticOperations(self.num1, self.num2, self.bits)
        ops.show_addition_result(8, "00001000")

    def test_show_number_info(self):
        ops = ArithmeticOperations(self.num1, self.num2, self.bits)
        ops.show_number_info(5)


class TestBinaryOperations(unittest.TestCase):
    def setUp(self):
        self.num1 = 5
        self.num2 = 3
        self.bits = 8

    def test_multiply_in_direct_code_positive(self):
        ops = BinaryOperations(self.num1, self.num2, self.bits)
        result_decimal, result_binary = ops.multiply_in_direct_code()
        self.assertEqual(result_decimal, 15)
        self.assertEqual(result_binary, "00001111")

    def test_multiply_in_direct_code_negative(self):
        ops = BinaryOperations(-self.num1, self.num2, self.bits)
        result_decimal, result_binary = ops.multiply_in_direct_code()
        self.assertEqual(result_decimal, -15)
        self.assertEqual(result_binary, "10001111")

    def test_multiply_in_direct_code_overflow(self):
        ops = BinaryOperations(64, 4, 8)
        with self.assertRaises(OverflowError):
            ops.multiply_in_direct_code()

    def test_divide_with_precision_positive(self):
        ops = BinaryOperations(self.num1, self.num2, self.bits)
        result_decimal, result_binary = ops.divide_with_precision()
        self.assertIsInstance(result_decimal, float)
        self.assertIsInstance(result_binary, str)
        self.assertIn(".", result_binary)

    def test_divide_with_precision_negative(self):
        ops = BinaryOperations(-self.num1, self.num2, self.bits)
        result_decimal, result_binary = ops.divide_with_precision()
        self.assertIsInstance(result_decimal, float)
        self.assertIsInstance(result_binary, str)
        self.assertIn(".", result_binary)
        self.assertEqual(result_binary[0], "1")

    def test_divide_by_zero(self):
        ops = BinaryOperations(self.num1, 0, self.bits)
        with self.assertRaises(ZeroDivisionError):
            ops.divide_with_precision()

    def test_get_direct_code(self):
        ops = BinaryOperations(self.num1, self.num2, self.bits)
        self.assertEqual(ops.get_direct_code(5), "00000101")
        self.assertEqual(ops.get_direct_code(-5), "10000101")

    def test_show_multiplication_result(self):
        ops = BinaryOperations(self.num1, self.num2, self.bits)
        ops.show_multiplication_result(15, "00001111")

    def test_show_number_info(self):
        ops = BinaryOperations(self.num1, self.num2, self.bits)
        ops.show_number_info(5)


class TestFloatingPointIEEE754(unittest.TestCase):
    def setUp(self):
        self.num1 = 12.5
        self.num2 = 1.25
        self.negative_num = -3.75

    def test_float_to_ieee754_positive(self):
        converter = FloatingPointIEEE754(self.num1, self.num2)
        ieee = converter.float_to_ieee754(self.num1)
        self.assertEqual(ieee[:9], "010000010")
        self.assertEqual(len(ieee), 32)

    def test_float_to_ieee754_negative(self):
        converter = FloatingPointIEEE754(self.negative_num, self.num2)
        ieee = converter.float_to_ieee754(self.negative_num)
        self.assertEqual(ieee[0], "1")
        self.assertEqual(len(ieee), 32)

    def test_ieee754_to_float(self):
        converter = FloatingPointIEEE754(self.num1, self.num2)
        ieee = converter.float_to_ieee754(self.num1)
        result = converter.ieee754_to_float(ieee)
        self.assertAlmostEqual(result, self.num1, places=5)

    def test_add_ieee754_numbers(self):
        converter = FloatingPointIEEE754(self.num1, self.num2)
        ieee_sum = converter.add_ieee754_numbers()
        self.assertIsInstance(ieee_sum, str)
        self.assertEqual(len(ieee_sum), 32)

    def test_get_ieee754_sum(self):
        converter = FloatingPointIEEE754(self.num1, self.num2)
        ieee_sum = converter.get_ieee754_sum()
        self.assertIsInstance(ieee_sum, str)
        self.assertEqual(len(ieee_sum), 32)


if __name__ == '__main__':
    unittest.main()