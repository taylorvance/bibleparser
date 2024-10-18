import unittest

import sys
sys.path.append("..")

from bible_parser.bible import parse_reference, parse_parts


class TestParseReference(unittest.TestCase):
    def test_single_verse(self):
        self.assertEqual(parse_reference("John 3:16"), "John 3:16")
        self.assertEqual(parse_reference("john 3 16"), "John 3:16")
        self.assertEqual(parse_reference("john 3 verse 16"), "John 3:16")
        self.assertEqual(parse_reference("JOHN chapter 3 verse 16"), "John 3:16")

    def test_multiverse(self):
        self.assertEqual(parse_reference("John 3:16-17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3:16 thru 17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3:16 to 17"), "John 3:16-17")
        self.assertEqual(parse_reference("john chapter 3 verses 16 to 17"), "John 3:16-17")

    def test_chapter(self):
        self.assertEqual(parse_reference("1 John 3"), "1 John 3")
        self.assertEqual(parse_reference("1 john 3"), "1 John 3")
        self.assertEqual(parse_reference("1st JOHN chapter 3"), "1 John 3")
        self.assertEqual(parse_reference("first JOHN ch. 3"), "1 John 3")

    def test_book(self):
        self.assertEqual(parse_reference("2 Corinthians"), "2 Corinthians")
        self.assertEqual(parse_reference("second Corinthians"), "2 Corinthians")

    def test_number_words(self):
        self.assertEqual(parse_reference("one timothy four eight"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("won timothy for ate"), "1 Timothy 4:8")

    def test_ordinals(self):
        self.assertEqual(parse_reference("1 Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("first Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("1st Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("First Timothy 4:8"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("1st timothy 4 verse 8"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("first timothy chapter 4 verse 8"), "1 Timothy 4:8")

    def test_multiword(self):
        self.assertEqual(parse_reference("song of Solomon 4 5"), "Song Of Solomon 4:5")

    def test_whitespace(self):
        self.assertEqual(parse_reference(" john 3:16 "), "John 3:16")

    def test_missing_verse(self):
        self.assertEqual(parse_reference("John 3:"), "John 3")
        self.assertEqual(parse_reference("John chapter 3 verses"), "John 3")

    def test_synonyms(self):
        self.assertEqual(parse_reference("John chapter 3 v 16 through 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John ch. 3 vs. 16 through 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John ch 3 v. 16 through 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John 3 verses 16 to 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John 3:16 through 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John 3:16 thru 17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3 16 and 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John 3:16 - 17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3 16&17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3 16 17"), "John 3:16-17")
        self.assertEqual(parse_reference("John 3:16-17"), "John 3:16-17")


if __name__ == '__main__':
    unittest.main()
