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

## LinkML

This repo also includes a LinkML schema for describing the official JSON-LD test suite.
Feel free to re-use this for generating code that relates to these entities.

## Documentation

API docs are available at **<https://multimeric.github.io/json-ld-test/>**.

## JSON-LD License

Use of the JSON-LD test suite, originally from https://w3c.github.io/json-ld-api/tests/ is licensed under the [W3C Software and Document License](https://www.w3.org/copyright/software-license-2023/).