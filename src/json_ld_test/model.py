from dataclasses import dataclass
from importlib import resources

@dataclass
class NegativeMixin:
    """
    Added to a test case to indicate that it should fail
    """
    expect_error_code: str

@dataclass
class TestCase:
    name: str
    purpose: str
    # spec_version: str
    #: Relative path to the input document
    input: str

    @staticmethod
    def read_file(path: str) -> str:
        return resources.open_text(__name__, path).read()

    @property
    def input_contents(self) -> str:
        return self.read_file(self.input)

@dataclass
class PositiveMixin(TestCase):
    """
    Added to a test case to indicate that it should succeed
    """
    #: Relative path to the expected document
    expect: str

    @property
    def expect_contents(self) -> str:
        return self.read_file(self.expect)

@dataclass
class ContextTestCase(TestCase):
    #: Relative path to the context document
    context: str

    @property
    def context_contents(self) -> str:
        return self.read_file(self.context)

@dataclass
class OptionalContextTestCase(TestCase):
    context: str | None

    @property
    def context_contents(self) -> str | None:
        if self.context is not None:
            return self.read_file(self.context)

@dataclass
class PositiveCompactTest(ContextTestCase, PositiveMixin):
    pass

@dataclass
class NegativeCompactTest(ContextTestCase, NegativeMixin):
    pass
