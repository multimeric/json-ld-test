from json_ld_test import compact_tests, PositiveCompactTest, ContextTestCase
import json
import pytest

@pytest.mark.parametrize("test", compact_tests)
def test_compact(test: ContextTestCase):
    # Assert that everything is valid JSON
    json.loads(test.input_contents)
    json.loads(test.context_contents)
    if isinstance(test, PositiveCompactTest):
        json.loads(test.expect_contents)
