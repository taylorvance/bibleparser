# Bible Parser

Bible Parser is a Python library for parsing a Bible reference into a structured format. It is meant to disambiguate dictated references that may have been erroneously transcribed by Siri and other voice recognition software (e.g., "John 316" vs. "John 3:16").

## Quick Reference Commands
| **Action**                 | **Command**                          |
|--------------------------- |--------------------------------------|
| Create virtual environment | `python -m venv venv`                |
| Activate venv              | `source venv/bin/activate`           |
| Deactivate venv            | `deactivate`                         |
| Install package (editable) | `pip install -e .`                   |
| Run all tests              | `python -m unittest discover tests`  |
| Build the package          | `python -m build`                    |
| Upload to PyPI             | `twine upload dist/*`                |
