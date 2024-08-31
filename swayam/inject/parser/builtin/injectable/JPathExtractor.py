# This file is a part of Swayam
# Copyright 2015-2024 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
import json
from functools import partial
from jsonpath_ng.ext import parse as jparse

from swayam import Parser
from swayam.inject.structure import Structure

from swayam.inject.parser.parser import JsonContentParser

def extract_with_jpath(*, invoker, content, jpath:str, strict:str=True) -> str:
    """
    Extracts part of a JSON object with JPath.
    
    Args:
        content (str): The response from the LLM containing code blocks.
    """
    jsonpath_expr = jparse(jpath)
    matches = jsonpath_expr.find(content)
    if strict and not matches:
        raise Exception(f"No mmatch found using JPath {jpath} used for extraction from {content!r}.")
    return Structure.JsonContent(content=[match.value for match in matches])

JPathExtractor = partial(JsonContentParser,
    "JPathExtractor",
    callable=extract_with_jpath,
    input_structure=Structure.JsonContentParser,
    output_structure=Structure.JsonContent,
    content_structure=None
)