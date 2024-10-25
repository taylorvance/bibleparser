# Bible Parser

Bible Parser is a Python library for parsing a Bible reference into a structured format. It was designed to interpret dictated references that may have been mistranscribed by Siri or other voice recognition software (e.g., "John 316" becomes "John 3:16").


## Examples

Dictation                   | Transcription     | Parsed Reference
---------                   | -------------     | ----------------
john three sixteen          | John 316          | John 3:16
john three two through four | John 32 through 4 | John 3:2-4
matthew twenty one twelve   | Matthew 2112      | Matthew 21:12
first john one one          | 1st John 11       | 1 John 1:1
micah one one               | Michael 11        | Micah 1:1
jude one one                | June one one      | Jude 1:1
haggai two twenty three     | Hey guy 223       | Haggai 2:23
acts one twenty three       | X123              | Acts 1:23


## API

### Siri Shortcut
I originally created this project to use with a Siri Shortcut that accepts a Bible reference as input and returns the text of the passage.

### AWS Serverless API
I set up an AWS Lambda function behind an API Gateway to expose the functionality of this library as an HTTP API.

### Bible API by Tim Morgan
Special thanks to Tim Morgan for creating and hosting [bible-api](https://bible-api.com/)! My library merely parses the reference. Tim's API provides the actual text of the passage.


## Quick Reference Commands

Action                     | Command
------                     | -------
Create virtual environment | `python -m venv venv`
Activate venv              | `source venv/bin/activate`
Deactivate venv            | `deactivate`
Install package (editable) | `pip install -e .`
Run all tests              | `python -m unittest discover tests`
Build the package          | `python -m build`
Upload to PyPI             | `twine upload dist/*`
