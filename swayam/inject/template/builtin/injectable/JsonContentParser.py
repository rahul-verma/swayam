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

import json
from json import JSONDecodeError
from typing import Union
from pydantic import BaseModel, Field, field_serializer

from swayam import Template

from .JsonContent import JsonContentModel

## The methods used here are meant to prevent serialization warnings.
class JsonContentParserModel(JsonContentModel):
    
    jpath: str = Field(..., title="Jpath", description="JQuery path to find element(s) in the JSON content")
    strict: bool = Field(True, title="Strict Match", description="If True, raise an error if the JPath does not exist in the JSON content")
    
JsonContentParser = Template.build("JsonContentParser", model=JsonContentParserModel)