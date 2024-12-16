from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'https://w3c.github.io/json-ld-api/tests/',
     'id': 'https://w3c.github.io/json-ld-api/tests',
     'imports': ['linkml:types'],
     'name': 'TestSuite',
     'prefixes': {'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'jld': {'prefix_prefix': 'jld',
                          'prefix_reference': 'https://w3c.github.io/json-ld-api/tests/vocab#'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'mf': {'prefix_prefix': 'mf',
                         'prefix_reference': 'http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}}} )

class SpecVersion(str, Enum):
    json_ld_1FULL_STOP0 = "json-ld-1.0"
    json_ld_1FULL_STOP1 = "json-ld-1.1"


class Requires(str, Enum):
    I18nDatatype = "I18nDatatype"
    CompoundLiteral = "CompoundLiteral"
    GeneralizedRdf = "GeneralizedRdf"



class Manifest(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'mf:Manifest',
         'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    description: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['Manifest']} })
    sequence: List[Any] = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'sequence', 'domain_of': ['Manifest']} })


class TopLevelManifest(Manifest):
    """
    A manifest that contains a sequence of test manifests.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests',
         'slot_usage': {'sequence': {'name': 'sequence', 'range': 'string'}}})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    description: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['Manifest']} })
    sequence: List[str] = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'sequence', 'domain_of': ['Manifest']} })


class TestManifest(Manifest):
    """
    A manifest that contains a sequence of tests that all relate to a specific JSON-LD feature.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests',
         'slot_usage': {'sequence': {'any_of': [{'range': 'PositiveEvaluationTest'},
                                                {'range': 'NegativeEvaluationTest'},
                                                {'range': 'PositiveSyntaxTest'}],
                                     'name': 'sequence'}}})

    baseIri: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'baseIri', 'domain_of': ['TestManifest']} })
    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    description: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['Manifest']} })
    sequence: List[Union[NegativeEvaluationTest, PositiveEvaluationTest, PositiveSyntaxTest]] = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'sequence',
         'any_of': [{'range': 'PositiveEvaluationTest'},
                    {'range': 'NegativeEvaluationTest'},
                    {'range': 'PositiveSyntaxTest'}],
         'domain_of': ['Manifest']} })


class Test(ConfiguredBaseModel):
    """
    Abstract parent class for all test cases.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    purpose: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'purpose', 'domain_of': ['Test']} })
    input: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'input', 'domain_of': ['Test']} })
    option: Optional[Option] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'option', 'domain_of': ['Test']} })
    context: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'context', 'domain_of': ['Test']} })
    requires: Optional[Requires] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'requires', 'domain_of': ['Test']} })


class PositiveEvaluationTest(Test):
    """
    Describes a test case whose input is `input` and expects the output to be `expect`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    expect: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'expect', 'domain_of': ['PositiveEvaluationTest']} })
    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    purpose: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'purpose', 'domain_of': ['Test']} })
    input: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'input', 'domain_of': ['Test']} })
    option: Optional[Option] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'option', 'domain_of': ['Test']} })
    context: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'context', 'domain_of': ['Test']} })
    requires: Optional[Requires] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'requires', 'domain_of': ['Test']} })


class PositiveSyntaxTest(Test):
    """
    Describes a test case that only has to be parsed successfully to pass.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    purpose: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'purpose', 'domain_of': ['Test']} })
    input: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'input', 'domain_of': ['Test']} })
    option: Optional[Option] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'option', 'domain_of': ['Test']} })
    context: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'context', 'domain_of': ['Test']} })
    requires: Optional[Requires] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'requires', 'domain_of': ['Test']} })


class NegativeEvaluationTest(Test):
    """
    Describes a test case whose input is `input` and expects to raise an error with the message `expectErrorCode`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    expectErrorCode: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'expectErrorCode', 'domain_of': ['NegativeEvaluationTest']} })
    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Manifest', 'Test']} })
    purpose: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'purpose', 'domain_of': ['Test']} })
    input: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'input', 'domain_of': ['Test']} })
    option: Optional[Option] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'option', 'domain_of': ['Test']} })
    context: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'context', 'domain_of': ['Test']} })
    requires: Optional[Requires] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'requires', 'domain_of': ['Test']} })


class Option(ConfiguredBaseModel):
    """
    Captures all extra options that can be passed to a test.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    specVersion: Optional[SpecVersion] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'specVersion', 'domain_of': ['Option']} })
    processingMode: Optional[SpecVersion] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'processingMode', 'domain_of': ['Option']} })
    base: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'base', 'domain_of': ['Option']} })
    normative: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'normative', 'domain_of': ['Option']} })
    expandContext: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'expandContext', 'domain_of': ['Option']} })
    processorFeature: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'processorFeature', 'domain_of': ['Option']} })
    extractAllScripts: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'extractAllScripts', 'domain_of': ['Option']} })
    contentType: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'contentType', 'domain_of': ['Option']} })
    httpStatus: Optional[int] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'httpStatus', 'domain_of': ['Option']} })
    redirectTo: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'redirectTo', 'domain_of': ['Option']} })
    httpLink: Optional[Any] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'httpLink',
         'any_of': [{'multivalued': True}, {'multivalued': False}],
         'domain_of': ['Option']} })
    produceGeneralizedRdf: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'produceGeneralizedRdf', 'domain_of': ['Option']} })
    compactToRelative: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'compactToRelative', 'domain_of': ['Option']} })
    compactArrays: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'compactArrays', 'domain_of': ['Option']} })
    useNativeTypes: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'useNativeTypes', 'domain_of': ['Option']} })
    rdfDirection: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'rdfDirection', 'domain_of': ['Option']} })
    useRdfType: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'useRdfType', 'domain_of': ['Option']} })
    useJCS: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'useJCS', 'domain_of': ['Option']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Manifest.model_rebuild()
TopLevelManifest.model_rebuild()
TestManifest.model_rebuild()
Test.model_rebuild()
PositiveEvaluationTest.model_rebuild()
PositiveSyntaxTest.model_rebuild()
NegativeEvaluationTest.model_rebuild()
Option.model_rebuild()
