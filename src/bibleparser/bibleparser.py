import re
import urllib.request
import json

from difflib import get_close_matches

from .book_chapter_verses import book_chapter_verses


def parse_reference(text:str) -> str:
    """
    Interpret a reference string into a standardized format.
    """
    (book, chapter, verse_start, verse_end) = (x or "" for x in parse_parts(text))
    return f'{book} {chapter}:{verse_start}-{verse_end}'.strip(' :-')


def parse_parts(text:str) -> tuple:
    """
    Parse the book, chapter, and verses from a reference string.
    Returns a tuple of (book, chapter, verse_start, verse_end).
    """
    # Convert number words to digits.
    text = digitize(text)

    # Split on non-word characters.
    words = re.split(r'[^\w]+', text)

    # Filter out empty and filler words.
    ignore = {
        'chapter', 'ch',
        'verse', 'verses', 'vs', 'v',
        'through', 'thru', 'to',
        'the', 'a', 'an',
    }
    words = [w for w in words if w and w not in ignore]

    # Special case for "X123" and similar patterns. Siri confuses "Acts" for "X".
    m = re.match(r'^([xX])(\d+)', words[0])
    if m:
        words.insert(1, m.group(2))
        words[0] = m.group(1)

    book_words = []
    for i,word in enumerate(words):
        if i>0 and word.isdigit():
            # Break when we get to the first number word (except an ordinal at idx 0).
            break
        book_words.append(word)

    number_words = [word for word in words[1:] if word.isdigit()]

    book = ' '.join(book_words)
    chapter = int(number_words.pop(0)) if number_words else None
    verse_start = int(number_words.pop(0)) if number_words else None
    verse_end = int(number_words.pop(0)) if number_words else None

    book = format_book(book)
    if not book:
        raise ValueError(f'Could not parse book from "{text}".')

    return range_check((book, chapter, verse_start, verse_end))

def range_check(parts:tuple) -> tuple:
    """
    If the chapter number is out of the book's range, split it into chapter and verse.
    Sometimes dictation is ambiguous. Dictating "Matthew twenty one twelve" is sometimes transcribed as "Matthew 2112" instead of "Matthew 21:12".
    """
    (book, chapter, verse_start, verse_end) = parts
    if not chapter:
        return parts

    booklow = book.lower()
    if booklow not in book_chapter_verses:
        return parts

    max_chapter = max(book_chapter_verses[booklow].keys())
    max_verse = book_chapter_verses[booklow][max_chapter]

    if chapter > max_chapter:
        chapterstr = str(chapter)
        if len(chapterstr) == 4:
            verse_end = verse_start
            verse_start = int(chapterstr[2:])
            chapter = int(chapterstr[:2])
        elif len(chapterstr) == 3:
            verse_end = verse_start
            verse_start = int(chapterstr[1:])
            chapter = int(chapterstr[0])
        elif len(chapterstr) == 2:
            verse_end = verse_start
            verse_start = int(chapterstr[1:])
            chapter = int(chapterstr[0])

    return (book, chapter, verse_start, verse_end)


def digitize(text:str) -> str:
    """
    Convert number words (from one to ninety-nine) to digits.
    Supports certain homophones.
    """
    ones = {
        'one':'1', 'won':'1', 'went':'1',
        'two':'2', # Don't convert to/too, as that may be part of a verse range (eg. "Genesis 1 1 to 3").
        'three':'3',
        'four':'4', 'for':'4',
        'five':'5',
        'six':'6', 'sicks':'6',
        'seven':'7',
        'eight':'8', 'ate':'8',
        'nine':'9',
    }
    tens = {
        'twenty':'20',
        'thirty':'30',
        'forty':'40', 'fourty':'40',
        'fifty':'50',
        'sixty':'60',
        'seventy':'70',
        'eighty':'80',
        'ninety':'90',
    }

    # Handle composite numbers like "forty-two".
    def digitize_composite(m):
        parts = m.group(0).lower().split('-')
        return str(int(tens[parts[0]]) + int(ones[parts[1]]))
    pattern = r'\b(' + '|'.join(re.escape(key) for key in tens.keys()) + r')-(' + '|'.join(re.escape(key) for key in ones.keys()) + r')\b'
    text = re.sub(pattern, digitize_composite, text, flags=re.IGNORECASE)

    # Handle single numbers.
    word2num = {
        **ones,
        **tens,
        **{
        'ten':'10',
        'eleven':'11',
        'twelve':'12',
        'thirteen':'13',
        'fourteen':'14',
        'fifteen':'15',
        'sixteen':'16',
        'seventeen':'17',
        'eighteen':'18',
        'nineteen':'19',
    }}
    pattern = r'\b(' + '|'.join(re.escape(key) for key in word2num.keys()) + r')\b'
    text = re.sub(pattern, lambda m: word2num[m.group(0).lower()], text, flags=re.IGNORECASE)

    return text


def format_book(book:str) -> str:
    """
    Format the book name into a standardized format.
    Handles various synonyms, homophones, and misspellings.
    """
    # Convert to lowercase and split on whitespace.
    words = book.strip().lower().split()

    # If the first word is an ordinal, convert it to a number.
    ord2num = {
        '1st':'1', 'first':'1', 'one':'1', 'won':'1',
        '2nd':'2', 'second':'2', 'two':'2', 'to':'2', 'too':'2',
        '3rd':'3', 'third':'3', 'three':'3',
    }
    if words[0] in ord2num:
        words[0] = ord2num[words[0]]

    book = ' '.join(words)

    if book not in book_chapter_verses:
        # Check for synonyms (psalm vs psalms, song of songs vs song of solomon), homophones (jon vs john), misinterpretations (june vs jude), etc.
        # These will map to the official book name in the book_chapter_verses dict.
        tocanon = {
            'roof':'ruth',
            'psalm':'psalms', 'song':'psalms', 'songs':'psalms',
            'proverb':'proverbs',
            'song of songs':'song of solomon',
            'name':'nahum',
            'aim us':'amos', 'a moss':'amos', 'moss':'amos',
            'habacuc':'habakkuk', 'habit cook':'habakkuk',
            'hey guy':'haggai', 'hi guy':'haggai', 'hag eye':'haggai', 'haggy eye':'haggai',
            'marc':'mark',
            'x':'acts', 'ax':'acts', 'axe':'acts', 'ask':'acts',
            'jon':'john', '1 jon':'1 john', '2 jon':'2 john', '3 jon':'3 john',
            'phillipians':'philippians',
            'tight us':'titus', 'tied us':'titus',
            'june':'jude',
            'revelations':'revelation',
        }
        book = tocanon.get(book, book)

    if book not in book_chapter_verses:
        # Find closest match (with at least 60% similarity).
        matches = get_close_matches(book, book_chapter_verses.keys(), n=1, cutoff=0.6)
        book = matches[0] if matches else book

    # Return the book, title-cased.
    return book.title()


def fetch_passage(text:str) -> dict:
    passage = parse_reference(text)
    if not passage:
        return None

    url = f'https://bible-api.com/{urllib.parse.quote(passage)}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        data = res.read().decode('utf-8')
        data = json.loads(data)

    return {
        'input': text,
        'parsed': passage,
        'reference': data['reference'],
        'text': data['text'],
    }

def get_passage(text:str) -> str:
    return fetch_passage(text)['text']
