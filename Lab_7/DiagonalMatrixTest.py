import unittest
from DiagonalMatrix import DiagonalMatrix


class TestDiagonalMatrix(unittest.TestCase):

    def setUp(self):
        self.matrix = DiagonalMatrix(16, 16)

    def test_set_word_and_get_word(self):
        self.matrix.set_word([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
        self.assertEqual(self.matrix.get_word(0, 0, 16), [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_set_index_colum_and_get_index_column(self):
        self.matrix.set_index_colum([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
        self.assertEqual(self.matrix.get_index_column(0, 0, 16), [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_logical_and(self):
        self.matrix.set_word([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
        self.matrix.set_word([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 1, 1)
        self.assertEqual(self.matrix.logical_and(0, 1), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_logical_nand(self):
        self.matrix.set_word([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
        self.matrix.set_word([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 1, 1)
        self.assertEqual(self.matrix.logical_nand(0, 1), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def test_repeat_first_arg(self):
        self.matrix.set_word([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
        self.assertEqual(self.matrix.repeat_first_arg(0), [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_negate_first_arg(self):
        self.matrix.set_word([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
        self.assertEqual(self.matrix.negate_first_arg(0), [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

    def test_add_binary(self):
        self.assertEqual(self.matrix.add_binary([1, 1, 0], [1, 0, 1]), [1, 0, 1, 1])

    def test_sum_fields(self):
        # Устанавливаем тестовые слова с ключом [1, 1, 0]
        # Формат слова: V(3 бита) A(4 бита) B(4 бита) S(5 бит)

        # Первое слово: V=110, A=1010 (10), B=0101 (5), S=00000
        self.matrix.set_word([1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], 0, 0)

        # Второе слово: V=110, A=0101 (5), B=0101 (5), S=00000
        self.matrix.set_word([1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0], 1, 1)

        self.matrix.sum_fields([1, 1, 0])

        # Проверяем первое слово:
        # A=1010 (10) + B=0101 (5) = 15 (01111)
        expected_word1 = [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1]
        self.assertEqual(self.matrix.get_word(0, 0, 16), expected_word1)

        # Проверяем второе слово:
        # A=0101 (5) + B=0101 (5) = 10 (01010)
        expected_word2 = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(self.matrix.get_word(1, 1, 16), expected_word2)


    def test_find_nearest(self):
        self.matrix.set_word([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 0)  # 0
        self.matrix.set_word([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 1, 1)  # 1
        self.matrix.set_word([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 2, 2)  # 2
        self.matrix.set_word([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 3, 3)  # 4

        target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]  # 1

        # Ближайшее сверху (больше чем 1) должно быть 2
        nearest_up = self.matrix.find_nearest(target, direction="up")
        self.assertEqual(nearest_up, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])

        # Ближайшее снизу (меньше чем 1) должно быть 0
        nearest_down = self.matrix.find_nearest(target, direction="down")
        self.assertEqual(nearest_down, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()