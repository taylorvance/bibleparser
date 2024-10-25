import unittest

import sys
sys.path.append("..")

from bibleparser.bibleparser import parse_reference


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
        self.assertEqual(parse_reference("john 3:16 and 17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3:16 & 17"), "John 3:16-17")
        self.assertEqual(parse_reference("john 3:16&17"), "John 3:16-17")
        self.assertEqual(parse_reference("john chapter 3 verses 16 to 17"), "John 3:16-17")

    def test_chapter(self):
        self.assertEqual(parse_reference("1 John 3"), "1 John 3")
        self.assertEqual(parse_reference("1 john 3"), "1 John 3")
        self.assertEqual(parse_reference("1st JOHN chapter 3"), "1 John 3")
        self.assertEqual(parse_reference("first JOHN ch. 3"), "1 John 3")

    def test_book(self):
        self.assertEqual(parse_reference("2 Corinthians"), "2 Corinthians")
        self.assertEqual(parse_reference("second Corinthians"), "2 Corinthians")
        self.assertEqual(parse_reference("two Corinthians"), "2 Corinthians")

    def test_number_words(self):
        self.assertEqual(parse_reference("one timothy four eight"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("won timothy for ate"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("psalm nineteen"), "Psalms 19")
        self.assertEqual(parse_reference("matthew 12 went through eight"), "Matthew 12:1-8")

    def test_composite_numbers(self):
        self.assertEqual(parse_reference("psalm forty-two"), "Psalms 42")
        self.assertEqual(parse_reference("psalm forty two"), "Psalms 40:2")
        self.assertEqual(parse_reference("psalm fourty-won"), "Psalms 41")
        self.assertEqual(parse_reference("matthew twenty twenty"), "Matthew 20:20")
        self.assertEqual(parse_reference("psalm ninety-nine nine"), "Psalms 99:9")

    def test_ordinals(self):
        self.assertEqual(parse_reference("1 Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("first Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("1st Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("one Timothy"), "1 Timothy")
        self.assertEqual(parse_reference("First Timothy 4:8"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("1st timothy 4 verse 8"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("first timothy chapter 4 verse 8"), "1 Timothy 4:8")
        self.assertEqual(parse_reference("two corinthians one two to three"), "2 Corinthians 1:2-3")

    def test_multiword(self):
        self.assertEqual(parse_reference("song of Solomon 4 5"), "Song Of Solomon 4:5")
        self.assertEqual(parse_reference("song of Solomon four five"), "Song Of Solomon 4:5")

    def test_whitespace(self):
        self.assertEqual(parse_reference(" john  3  16 "), "John 3:16")

    def test_special_chars(self):
        self.assertEqual(parse_reference("mark, 1, 1"), "Mark 1:1")
        self.assertEqual(parse_reference("\"mark, 1, 1\""), "Mark 1:1")
        self.assertEqual(parse_reference("'mark, 1, 1'"), "Mark 1:1")

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

    def test_range_check(self):
        self.assertEqual(parse_reference("matthew 512"), "Matthew 5:12") # "matthew five twelve"
        self.assertEqual(parse_reference("matthew 512 through 15"), "Matthew 5:12-15") # "matthew five twelve through fifteen"
        self.assertEqual(parse_reference("matthew 2112"), "Matthew 21:12") # "matthew twenty one twelve"
        self.assertEqual(parse_reference("matthew 2112 to 13"), "Matthew 21:12-13") # "matthew twenty one twelve to thirteen"
        self.assertEqual(parse_reference("matthew 33 to 12"), "Matthew 3:3-12") # "matthew three three to twelve"
        self.assertEqual(parse_reference("deuteronomy 2020"), "Deuteronomy 20:20") # "deuteronomy twenty twenty"
        self.assertEqual(parse_reference("second kings 2020 through 21"), "2 Kings 20:20-21") # "second kings twenty twenty through twenty one"
        self.assertEqual(parse_reference("psalms 3820"), "Psalms 38:20") # "psalms thirty eight twenty"
        self.assertEqual(parse_reference("psalms 3820 through 22"), "Psalms 38:20-22") # "psalms thirty eight twenty through twenty two"
        self.assertEqual(parse_reference("song of solomon 45"), "Song Of Solomon 4:5")
        # self.assertEqual(parse_reference("Psalms 156"), "Psalms 150:6") #."psalms one fifty six" doesn't work with current implementation

    def test_canonicalization(self):
        self.assertEqual(parse_reference("Psalm 1 1"), "Psalms 1:1")
        self.assertEqual(parse_reference("Proverb 1 1"), "Proverbs 1:1")
        self.assertEqual(parse_reference("the song of songs 1 1"), "Song Of Solomon 1:1")
        self.assertEqual(parse_reference("ax 1 1"), "Acts 1:1")
        self.assertEqual(parse_reference("axe 1 1"), "Acts 1:1")
        self.assertEqual(parse_reference("X126"), "Acts 1:26")
        self.assertEqual(parse_reference("Jon 1 1"), "John 1:1")
        self.assertEqual(parse_reference("1st Jon 1 1"), "1 John 1:1")
        self.assertEqual(parse_reference("First Jon 1 1"), "1 John 1:1")
        self.assertEqual(parse_reference("Revelations 1 1"), "Revelation 1:1")

    def test_close_matches(self):
        self.assertEqual(parse_reference("join 3 16"), "John 3:16")
        self.assertEqual(parse_reference("first join 3 16"), "1 John 3:16")
        self.assertEqual(parse_reference("Hag I one one"), "Haggai 1:1")
        self.assertEqual(parse_reference("Hag eye one one"), "Haggai 1:1")
        self.assertEqual(parse_reference("Hey guy 223"), "Haggai 2:23")
        self.assertEqual(parse_reference("gen 1 1"), "Genesis 1:1")
        self.assertEqual(parse_reference("1st Tessa 4 8"), "1 Thessalonians 4:8")
        self.assertEqual(parse_reference("Michael 1 1"), "Micah 1:1")


if __name__ == '__main__':
    unittest.main()
