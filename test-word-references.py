import unittest
from word_references import WordReferences


class TestWordReferences(unittest.TestCase):

    def test_should_be_exception_on_term_none(self):
        self.assertRaises(AttributeError, WordReferences, None)
        self.assertRaises(AttributeError, WordReferences, "")

    def test_instance_by_source(self):
        service = WordReferences("hello", "<h1>Test</h1>")
        self.assertIsInstance(service, WordReferences,
                              "Should be instance of WordReferences")


if __name__ == "__main__":
    unittest.main()
