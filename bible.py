import re
import urllib.request
import json


def parse_reference(text:str) -> str:
    (book, chapter, verse_start, verse_end) = parse_parts(text)
    # print(f'"{text}" => {book}/{chapter}/{verse_start}/{verse_end}')

    book = format_book(book)
    if not book:
        raise ValueError(f'Could not parse book from "{text}".')

    if not chapter: return f'{book}'
    if not verse_start: return f'{book} {chapter}'
    if not verse_end: return f'{book} {chapter}:{verse_start}'
    return f'{book} {chapter}:{verse_start}-{verse_end}'


def parse_parts(text:str) -> tuple:
    # Convert number words to integers.
    text = convert_numbers(text)

    # Split on whitespace, colons, hyphens, ampersands, and periods.
    words = re.split(r'[\s:\-&\.]', text)

    # Filter out empty and filler words.
    ignore = {
        'chapter', 'ch',
        'verse', 'verses', 'vs', 'v',
        'through', 'thru', 'to',
    }
    words = [word for word in words if word and word not in ignore]

    book_words = []
    for i,word in enumerate(words):
        if i>0 and word.isdigit():
            # Break when we get to the first number word (except an ordinal at idx 0).
            break
        book_words.append(word)

    number_words = [word for word in words[1:] if word.isdigit()]

    book = ' '.join(book_words)
    chapter = number_words.pop(0) if number_words else None
    verse_start = number_words.pop(0) if number_words else None
    verse_end = number_words.pop(0) if number_words else None

    return (book, chapter, verse_start, verse_end)

def _old_parse_parts(text:str) -> tuple:
    chapter_synonyms = '|'.join(['chapter','ch'])
    verse_synonyms = '|'.join([':','verse','verses','vs','v'])
    through_synonyms = '|'.join(['through','thru','to','-'])

    pattern = rf'^\s*(?P<book>[1-3]?[A-Za-z ]+?)\s*(?:{chapter_synonyms})?\.?\s*(?P<chapter>\d+)?\s*(?:{verse_synonyms}?)?\.?\s*(?P<verse_start>\d+)?\s*(?:(?:{through_synonyms})\s*(?P<verse_end>\d+))?\s*$'

    match = re.match(pattern, convert_numbers(text), re.IGNORECASE)
    if not match:
        raise ValueError(f'Could not parse reference from "{text}".')

    book = match.group('book')
    chapter = match.group('chapter')
    verse_start = match.group('verse_start')
    verse_end = match.group('verse_end')

    return (book, chapter, verse_start, verse_end)


def convert_numbers(text:str) -> str:
    word2num = {
        'one':'1', 'won':'1',
        'two':'2', # Don't convert to/too, as that may be part of a verse range (eg. "Genesis 1 1 to 3").
        'three':'3',
        'four':'4', 'for':'4',
        'five':'5',
        'six':'6', 'sicks':'6',
        'seven':'7',
        'eight':'8', 'ate':'8',
        'nine':'9',
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
        'twenty':'20',
    }
    pattern = r'\b(' + '|'.join(re.escape(key) for key in word2num.keys()) + r')\b'
    return re.sub(pattern, lambda match: word2num[match.group(0).lower()], text, flags=re.IGNORECASE)


def format_book(text:str) -> str:
    words = text.strip().lower().split()

    # Format ordinals as plain numbers.
    ord2num = {
        '1st':'1', 'first':'1',
        '2nd':'2', 'second':'2',
        '3rd':'3', 'third':'3',
    }
    words[0] = ord2num.get(words[0], words[0])

    book = ' '.join(words)

    # Validate against the list of books.

    book = book.title() #.temp

    return book


def fetch_passage(text:str) -> dict:
    passage = parse_reference(text)
    if not passage:
        return None

    # print(f'fetching {passage}')
    url = f'https://bible-api.com/{urllib.parse.quote(passage)}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        data = res.read().decode('utf-8')
        data = json.loads(data)
    # print(json.dumps(data, indent=4))

    return {
        'input': text,
        'parsed': passage,
        'reference': data['reference'],
        'text': data['text'],
    }

def get_passage(text:str) -> str:
    return fetch_passage(text)['text']
