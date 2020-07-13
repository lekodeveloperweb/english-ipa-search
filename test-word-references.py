import unittest
from word_references import WordReferences


class TestWordReferences(unittest.TestCase):

    def setUp(self):
        self.reader = open("data/you.html")
        self.source = self.reader.read()
        self.service = WordReferences("you", self.source)

    def tearDown(self):
        self.reader.close()

    def test_should_be_exception_on_term_none(self):
        self.assertRaises(AttributeError, WordReferences, None)
        self.assertRaises(AttributeError, WordReferences, "")
        self.assertRaises(AttributeError, WordReferences, " ")

    def test_instance_by_source(self):
        self.assertIsInstance(self.service, WordReferences,
                              "Should be instance of WordReferences")

    def test_remove_word_spaces_and_characters(self):
        service = WordReferences("you. !?^ .,_-!", self.source)
        self.assertEqual(len(service._words), 1)

    def test_get_search_types(self):
        types = self.service.get_search_types()
        self.assertEqual(len(types), 5)
        self.assertEqual(types[1], "DEFINITION")

    def test_set_search_type_unknow_exit(self):
        with self.assertRaises(SystemExit) as se:
            self.service.set_search_type("10")
        self.assertEqual(se.exception.code, 1)

    def test_set_search_type(self):
        self.service.set_search_type("1")
        self.assertEqual(self.service._selected_search_type, "DEFINITION")

    def test_extract_pronunciation_error_on_search_type_none(self):
        self.assertRaises(AttributeError, self.service.extract_pronunciation,
                          None)
        self.assertRaises(AttributeError, self.service.extract_pronunciation,
                          "")
        self.assertRaises(AttributeError, self.service.extract_pronunciation,
                          " ")

    def test_extract_pronunciation_change_type_to_one(self):
        self.service.extract_pronunciation("10")
        self.assertEqual(self.service._selected_search_type, "DEFINITION")

    def test_extract_pronunciation(self):
        pronunciations = self.service.extract_pronunciation("1")
        self.assertEqual(len(pronunciations), 1)
        self.assertEqual(pronunciations[0][0].pronounce, "/ˈjuː/")
        self.assertEqual(pronunciations[0][0].type_pronun, "strong")


if __name__ == "__main__":
    unittest.main()
