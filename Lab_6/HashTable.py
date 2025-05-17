class HashTable:
    def __init__(self, size):
        self.alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        self.table_size = size
        self.table = [[] for _ in range(size)]  # Теперь каждая ячейка — список

    def __value_of_key(self, key):
        if len(key) < 2:
            raise ValueError("Ключ должен быть длиннее 2 символов.")
        if not (key[0].upper() in self.alphabet and key[1].upper() in self.alphabet):
            raise ValueError("Первые два символа ключа должны быть буквы русского алфавита")
        base = len(self.alphabet)
        v = self.alphabet.index(key[0].upper()) * base + self.alphabet.index(key[1].upper())
        return v

    def __hash(self, key):
        return self.__value_of_key(key) % self.table_size

    def insert(self, key, value):
        hash_index = self.__hash(key)
        chain = self.table[hash_index]
        # Проверяем, нет ли уже такого ключа в цепочке
        for i, (existing_key, _) in enumerate(chain):
            if existing_key == key:
                chain[i] = (key, value)  # Обновляем значение, если ключ найден
                return
        chain.append((key, value))  # Добавляем новую пару, если ключа не было

    def search(self, key):
        hash_index = self.__hash(key)
        chain = self.table[hash_index]
        for existing_key, value in chain:
            if existing_key == key:
                return value
        return None  # Ключ не найден

    def delete(self, key):
        hash_index = self.__hash(key)
        chain = self.table[hash_index]
        for i, (existing_key, _) in enumerate(chain):
            if existing_key == key:
                del chain[i]  # Удаляем элемент из цепочки
                return
        raise KeyError("Нет такого ключа.")

    def update(self, key, value):
        hash_index = self.__hash(key)
        chain = self.table[hash_index]
        for i, (existing_key, _) in enumerate(chain):
            if existing_key == key:
                chain[i] = (key, value)  # Обновляем значение
                return
        raise KeyError("Нет такого ключа.")


# Пример использования
table = HashTable(10)
table.insert("Дима", "Плотник")
table.insert("ДимаКоллизия", "Актер")  # Попадёт в ту же ячейку, что и "Дима"
table.insert("Рома", "Слесарь")

print(table.search("Дима"))           # Вывод: Плотник
print(table.search("ДимаКоллизия"))   # Вывод: Актер
print(table.search("Рома"))           # Вывод: Слесарь

table.update("Дима", "Программист")
print(table.search("Дима"))           # Вывод: Программист

table.delete("Рома")
print(table.search("Рома"))           # Вывод: None

try:
    table.update("Олег", "Повар")
except KeyError as e:
    print(f"Ошибка: {e}")  # Выведет: Ошибка: Нет такого ключа.

try:
    table.delete("Олег")
except KeyError as e:
    print(f"Ошибка: {e}")  # Выведет: Ошибка: Нет такого ключа.

try:
    table.insert("John", "Программист")
except ValueError as e:
    print(f"Ошибка: {e}")  # Выведет: Ошибка: Первые два символа ключа должны быть буквы русского алфавита

try:
    table.insert("Я", "Тестировщик")
except ValueError as e:
    print(f"Ошибка: {e}")  # Выведет: Ошибка: Ключ должен быть длиннее 2 символов.