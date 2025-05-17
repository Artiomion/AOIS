class DiagonalMatrix:
    def __init__(self, rows, cols):
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.colums = cols

    def set_word(self, word, start_row, col):
        for i, val in enumerate(word):
            row = (start_row + i) % self.rows
            self.matrix[row][col] = val

    def set_index_colum(self, index, start_row, start_colum):
        for i, val in enumerate(index):
            self.matrix[(start_row + i) % self.rows][(start_colum + i) % self.colums] = val

    def get_word(self, start_row, col, length):
        return [self.matrix[(start_row + i) % self.rows][col] for i in range(length)]

    def get_index_column(self, start_row, start_colum, length):
        return [self.matrix[(start_row + i) % self.rows][(start_colum + i) % self.colums] for i in range(length)]

    def logical_and(self, col1, col2):  # f1 и
        word1 = self.get_word(col1, col1, self.rows)
        word2 = self.get_word(col2, col2, self.rows)
        return [int(word1[i] & word2[i]) for i in range(self.rows)]

    def logical_nand(self, col1, col2):  # f14 и-не
        word1 = self.get_word(col1, col1, self.rows)
        word2 = self.get_word(col2, col2, self.rows)
        return [int(not (word1[i] & word2[i])) for i in range(self.rows)]

    def repeat_first_arg(self, col1):  # f3 повторение аргумента
        word = self.get_word(col1, col1, self.rows)
        return word.copy()  # Просто повторяет слово

    def negate_first_arg(self, col1):  # f12 не для 1-го аругмента
        word = self.get_word(col1, col1, self.rows)
        return [int(not bit) for bit in word]

    def add_binary(self, a, b):
        result = []
        carry = 0
        for i in range(len(a) - 1, -1, -1):
            total = a[i] + b[i] + carry
            result.insert(0, total % 2)
            carry = total // 2
        if carry:
            result.insert(0, carry)
        return result

    def sum_fields(self, key_bits):
        key_len = len(key_bits)
        for col in range(self.colums):
            word = self.get_word(col, col, self.rows)
            if word[:key_len] == key_bits:
                # Разбиваем слово на поля: V (3 бита), A (4 бита), B (4 бита), S (5 бит)
                V = word[:key_len]
                A = word[key_len:key_len + 4]
                B = word[key_len + 4:key_len + 8]
                S = word[key_len + 8:key_len + 13]

                sum_result = self.add_binary(A, B)

                sum_result = sum_result[-5:]
                if len(sum_result) < 5:
                    sum_result = [0] * (5 - len(sum_result)) + sum_result

                new_word = V + A + B + sum_result
                self.set_word(new_word, col, col)

    def compare(self, value1: list[int], value2: list[int]):
        for i in range(len(value1)):
            if value1[i] > value2[i]:
                return 1
            elif value1[i] < value2[i]:
                return -1
        return 0

    def find_nearest(self, target_word, direction="up"):
        min_diff = float('inf')
        nearest_word = None
        diagonal_words = []
        for col in range(self.colums):
            word = self.get_word(col, col, self.rows)
            diagonal_words.append((col, word))
        for col, word in diagonal_words:
            comparison = self.compare(target_word, word)
            if direction == "up" and comparison > 0:
                if comparison < min_diff:
                    min_diff = comparison
                    nearest_word = word
            elif direction == "down" and comparison < 0:
                if -comparison < min_diff:
                    min_diff = -comparison
                    nearest_word = word
        return nearest_word


matrix = DiagonalMatrix(16, 16)
for row in matrix.matrix:
    print(row)


matrix.set_word([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0], 0, 0)
#matrix.set_word([1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1], 0, 0)
matrix.set_word([1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 1, 1)
matrix.set_word([0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], 2, 2)
matrix.set_index_colum([0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], 1, 0)
matrix.set_index_colum([1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1], 3, 1)
print("Матрица после записи слов и адресных столбцов:")
for row in matrix.matrix:
    print(row)

print("Слово из столбца 0:", matrix.get_word(0, 0, 16))
print("Слово из столбца 1:", matrix.get_word(1, 1, 16))
print("Слово из столбца 2:", matrix.get_word(2, 2, 16))
print("Адресный столбец 1 из 0 столбца", matrix.get_index_column(1, 0, 16))
print("Адресный столбец 3 из 1 столбца", matrix.get_index_column(3, 1, 16))

print("Логическое И:   ", matrix.logical_and(1, 2))
print("Логическое И-НЕ:", matrix.logical_nand(1, 2))
print("Логическое ДА(для 1-го арг): ", matrix.repeat_first_arg(1))
print("Логическое НЕТ(для 1-го арг):", matrix.negate_first_arg(2))

matrix.sum_fields([1, 0, 1])
print("Матрица после сложения полей:")
for row in matrix.matrix:
    print(row)

# Корректный вызов find_nearest:
target = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1] # 23 131
print("Ближайшее сверху:", matrix.find_nearest(target, direction="up"))
print("Ближайшее снизу:", matrix.find_nearest(target, direction="down"))


for i in range(16):
    word = ''.join(map(str, matrix.get_word(i, i, 16)))
    decimal = int(word, 2)
    print(f"Слово из столбца {i}: {word} (десятичное: {decimal})")


# #print("Слово из столбца 0:", ''.join(map(str, matrix.get_word(0, 0, 16))))
