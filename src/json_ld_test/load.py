from json_ld_test.models import TestManifest, Test
from linkml_runtime.loaders import JSONLoader
from typing import Literal, TypeAlias, cast
from importlib.resources import read_text

ManifestType: TypeAlias = Literal[
    "compact",
    "expand",
    "flatten",
    "fromRdf",
    "toRdf",
    "html",
    "remote-doc"
]

def get_manifest(manifest_type: ManifestType) -> TestManifest:
    """
    Load a test manifest
    Params: 
        manifest_type: The type of manifest to load, for example `compact`, `expand`, `flatten`, `fromRdf`, `toRdf`, `html`, or `remote-doc`.
    """
    content = read_text(__name__, f"{manifest_type}-manifest.jsonld")
    return cast(TestManifest, JSONLoader().load(content, TestManifest))

def get_test(test_name: str) -> Test:
    """
    Load a test by name
    Params:
        test_name: Name of the test to load, including the type prefix, for example `compact/0001-context.jsonld`.
            This is the form used in the manifest files, meaning that this function can be called directly from `some_manifest.sequence[some_index]`.
    """
    content = read_text(__name__, f"{test_name}-manifest.jsonld")
    return cast(Test, JSONLoader().load(content, Test))