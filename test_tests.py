from json_ld_test import compact_tests
import json

def test_compact():
    for test in compact_tests:
        # Assert that everything is valid JSON
        json.loads(test.input_contents)
