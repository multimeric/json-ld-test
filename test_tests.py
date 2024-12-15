from json_ld_test import get_test_file, get_all_tests, Test, PositiveEvaluationTest
import json
import pytest

def parse_from_name(name: str):
    return json.loads(get_test_file(name))

@pytest.mark.parametrize("test", get_all_tests(), ids=lambda test: test.name)
def test_everything(test: Test):
    """
    Assert that each test file is valid JSON by parsing it.
    In doing so, we also check that every manifest and every test file is valid JSON, is valid according to the Pydantic schema, and is loadable by the JSONLoader.
    """
    parse_from_name(test.input)
    if test.context is not None:
        parse_from_name(test.context)
    if isinstance(test, PositiveEvaluationTest):
        parse_from_name(test.expect)