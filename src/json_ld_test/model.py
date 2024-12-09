from dataclasses import dataclass
from importlib import resources

@dataclass
class TestCase:
    #: Relative path to the input document
    input: str
    #: Relative path to the expected document
    expect: str

    @property
    def input_contents(self) -> str:
        resources.open_text(self.input)

@dataclass
class ContextTestCase(TestCase):
    #: Relative path to the context document
    context: str

@dataclass
class OptionalContextTestCase(TestCase):
    context: str | None
