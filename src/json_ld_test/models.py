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



class Manifest(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mf:Manifest',
         'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Manifest', 'PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    description: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['Manifest']} })
    baseIri: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'baseIri', 'domain_of': ['Manifest']} })
    sequence: List[Union[NegativeEvaluationTest, PositiveEvaluationTest]] = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'sequence',
         'any_of': [{'range': 'PositiveEvaluationTest'},
                    {'range': 'NegativeEvaluationTest'}],
         'domain_of': ['Manifest'],
         'range_expression': {'any_of': [{'is_a': 'PositiveEvaluationTest'},
                                         {'is_a': 'NegativeEvaluationTest'}]}} })


class PositiveEvaluationTest(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'jld:PositiveEvaluationTest',
         'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Manifest', 'PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    purpose: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'domain_of': ['PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    input: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'input',
         'domain_of': ['PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    expect: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'expect', 'domain_of': ['PositiveEvaluationTest']} })
    option: Optional[Option] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'option',
         'domain_of': ['PositiveEvaluationTest', 'NegativeEvaluationTest']} })


class NegativeEvaluationTest(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'jld:NegativeEvaluationTest',
         'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    name: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Manifest', 'PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    purpose: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'domain_of': ['PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    input: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'input',
         'domain_of': ['PositiveEvaluationTest', 'NegativeEvaluationTest']} })
    expectErrorCode: str = Field(..., json_schema_extra = { "linkml_meta": {'alias': 'expectErrorCode', 'domain_of': ['NegativeEvaluationTest']} })
    option: Optional[Option] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'option',
         'domain_of': ['PositiveEvaluationTest', 'NegativeEvaluationTest']} })


class Option(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3c.github.io/json-ld-api/tests'})

    specVersion: Optional[SpecVersion] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'specVersion', 'domain_of': ['Option']} })
    processingMode: Optional[SpecVersion] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'processingMode', 'domain_of': ['Option']} })
    base: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'base', 'domain_of': ['Option']} })
    normative: Optional[bool] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'normative', 'domain_of': ['Option']} })
    expandContext: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'expandContext', 'domain_of': ['Option']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Manifest.model_rebuild()
PositiveEvaluationTest.model_rebuild()
NegativeEvaluationTest.model_rebuild()
Option.model_rebuild()
