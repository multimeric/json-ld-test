# JSON-LD-Test

Makes it easy to test the conformance of your JSON-LD parser by providing the official JSON-LD test suite as a Python package.

## Installation

```
pip install json-ld-test
```

## Example Usage

```python
from json_ld_test import get_all_tests, get_test_file

for test_case in get_all_tests():
    input = get_test_file(test_case.input)
    context = get_test_file(test_case.context)
    output = get_test_file(test_case.expected)
    assert parse_input(input, context) == output
```