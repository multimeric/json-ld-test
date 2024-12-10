from dataclasses import dataclass
from importlib import resources

@dataclass
class NegativeMixin:
    """
    Added to a test case to indicate that it should fail
    """
    expectErrorCode: str

@dataclass
class PositiveMixin:
    """
    Added to a test case to indicate that it should succeed
    """
    #: Relative path to the expected document
    expect: str

@dataclass
class TestCase:
    name: str
    purpose: str
    # spec_version: str
    #: Relative path to the input document
    input: str

    @property
    def input_contents(self) -> str:
        resources.open_text(__package__, self.input)

@dataclass
class ContextTestCase(TestCase):
    #: Relative path to the context document
    context: str

@dataclass
class OptionalContextTestCase(TestCase):
    context: str | None

@dataclass
class PositiveCompactTest(ContextTestCase, PositiveMixin):
    pass

@dataclass
class NegativeCompactTest(ContextTestCase, NegativeMixin):
    pass
