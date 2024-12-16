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

    Returns:
        An iterable of `ManifestType` objects, which are strings. Call `list()` on this to get a list of all manifest types.

    Examples:
        >>> list(get_manifest_types())
        ['compact', 'expand', 'flatten', 'fromRdf', 'toRdf', 'html', 'remote-doc']
    """
    # Extract the manifest options from the Literal ManifestType
    return ManifestType.__args__

def get_all_manifests() -> Iterable[TestManifest]:
    """
    Get each possible TestManifest

    Returns:
        An iterable of `TestManifest` objects. Call `list()` on this to get a list of all manifests.

    Examples:
        >>> len(list(get_all_manifests()))
        7
    """
    # Get the manifests for each type
    for t in get_manifest_types():
        yield get_manifest(t)

def get_all_tests() -> Iterable[Test]:
    """
    Get each possible Test

    Returns:
        An iterable of `Test` objects. Call `list()` on this to get a list of all tests.

    Examples:
        >>> len(list(get_all_tests()))
        1275
    """
    # Get all the tests from the manifests
    for m in get_all_manifests():
        yield from m.sequence

def get_manifest(manifest_type: ManifestType) -> TestManifest:
    """
    Load a specific test manifest

    Args: 
        manifest_type: The type of manifest to load as a string, for example `"compact"`.
        See `ManifestType`.
    
    Returns:
        The requested manifest object.

    Examples:
        >>> manifest = get_manifest("compact")
        >>> manifest.name
        'Compaction'
    """
    content = (anchor / f"{manifest_type}-manifest.jsonld").read_text()
    return cast(TestManifest, JSONLoader().load(content, TestManifest))

def get_test_file(test_name: str) -> str:
    """
    Load a specific test file by name

    Args:
        test_name: Name of the test file to load, including the type prefix, for example `compact/0001-context.jsonld`.
            You typically should only ever need to use `Test` object fields such as `input`, `context`, and `expect` for this argument.

    Returns:
        The content of the test file as a string.

    Examples:
        >>> manifest = get_manifest("compact")
        >>> some_test = manifest.sequence[0]
        >>> get_test_file(some_test.input)
        '{"@id": "http://example.org/test#example"}'
    """
    return (anchor / test_name).read_text()