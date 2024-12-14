from json_ld_test.models import Manifest
from linkml_runtime.loaders import JSONLoader
from typing import cast

def get_compact() -> Manifest:
    return cast(Manifest, JSONLoader().load("https://w3c.github.io/json-ld-api/tests/compact-manifest.jsonld", Manifest))