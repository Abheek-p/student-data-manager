import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contact_book as app


class ContactBookTests(unittest.TestCase):
    def test_next_id(self):
        contacts = [{"id": 1}, {"id": 3}]
        self.assertEqual(app.next_id(contacts), 4)

    def test_find_contact(self):
        contacts = [{"id": 7, "name": "Test"}]
        self.assertEqual(app.find_contact(contacts, "7")["name"], "Test")

    def test_missing_contact(self):
        self.assertIsNone(app.find_contact([], "1"))


if __name__ == "__main__":
    unittest.main()
