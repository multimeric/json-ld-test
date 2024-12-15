"""
Utilities for loading the JSON-LD test manifests and individual tests that are included in the package.
"""
from json_ld_test.models import TestManifest, Test
from linkml_runtime.loaders import JSONLoader
from typing import Iterable, Literal, TypeAlias, cast
from importlib.resources import files

anchor = files("json_ld_test")

ManifestType: TypeAlias = Literal[
    "compact",
    "expand",
    "flatten",
    "fromRdf",
    "toRdf",
    "html",
    "remote-doc"
]

def get_manifest_types() -> Iterable[ManifestType]:
    """
    Get the types of manifests that are available in the package.
    """
    # Extract the manifest options from the Literal ManifestType
    return ManifestType.__args__

def get_all_manifests() -> Iterable[TestManifest]:
    """
    Get each possible TestManifest
    """
    # Get the manifests for each type
    for t in get_manifest_types():
        yield get_manifest(t)

def get_all_tests() -> Iterable[Test]:
    """
    Get each possible Test
    """
    # Get all the tests from the manifests
    for m in get_all_manifests():
        yield from m.sequence

def get_manifest(manifest_type: ManifestType) -> TestManifest:
    """
    Load a specific test manifest
    Params: 
        manifest_type: The type of manifest to load, for example `compact`, `expand`, `flatten`, `fromRdf`, `toRdf`, `html`, or `remote-doc`.
    Example:
        manifest = get_manifest("compact")
    """
    content = (anchor / f"{manifest_type}-manifest.jsonld").read_text()
    return cast(TestManifest, JSONLoader().load(content, TestManifest))

def get_test_file(test_name: str) -> str:
    """
    Load a specific test file by name
    Params:
        test_name: Name of the test file to load, including the type prefix, for example `compact/0001-context.jsonld`.
            This is the form used the `Test` objects files.
    Returns:
        The content of the test file as a string.
    Example:
        manifest = get_manifest("compact")
        some_test = manifest.sequence[0]
        get_test_file(some_test.input)
    """
    return (anchor / test_name).read_text()