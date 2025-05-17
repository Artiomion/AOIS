import unittest
from HashTable import HashTable


class HashTableTest(unittest.TestCase):
    def test_init(self):
        table = None
        table = HashTable(5)
        self.assertIsNotNone(table)

    def test_insert(self):
        table = HashTable(20)
        table.insert("Дима", "Плотник")
        self.assertEqual(table.search("Дима"), "Плотник")

    def test_collision(self):
        table = HashTable(20)
        table.insert("Дима", "Плотник")
        table.insert("ДимаКоллизия", "Актер")
        self.assertEqual(table.search("Дима"), "Плотник")
        self.assertEqual(table.search("ДимаКоллизия"), "Актер")

    def test_delete(self):
        table = HashTable(20)
        table.insert("Дима", "Плотник")
        table.delete("Дима")
        self.assertEqual(table.search("Дима"), None)

    def test_update(self):
        table = HashTable(20)
        table.insert("Дима", "Плотник")
        table.update("Дима", "Фрилансер")
        self.assertEqual(table.search("Дима"), "Фрилансер")

