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

from swayam import Structure

_prefix = "PREFIX_"

## The methods used here are meant to prevent serialization warnings.
class JsonContentModel(BaseModel):
    
    content: str = Field(..., title="Json Text Content", description="Json object serialized into a string using json.dump/dumps.")
    
    @property
    def content(self) -> str:
        value = None
        # Automatically remove the prefix when fetching the value
        if self.__dict__['content'].startswith(_prefix):
            return self.__dict__['content'][len(_prefix):]
        else:
            return self.__dict__['content']

    @content.setter
    def content(self, v: str):
        # Automatically add the prefix when storing the value
        try:
            json.loads(v)
            self.__dict__['content'] = f"{_prefix}{v}"
        except JSONDecodeError as e:
            raise ValueError("Invalid content. Error:", e)
    
JsonContent, JsonContentList = Structure.build("JsonContent", model=JsonContentModel, return_composite=True)