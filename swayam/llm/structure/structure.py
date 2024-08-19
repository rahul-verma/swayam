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
from enum import Enum
from typing import *

from pydantic import BaseModel, create_model, Field


# Define a base class `Structure` that inherits from `BaseModel`
class IOStructure:
    
    def __init__(self, model:BaseModel):
        self.__data_model = model
        
    @property
    def data_model(self):
        return self.__data_model

    @property
    def definition(self):
        data_schema = self.data_model.model_json_schema()
        for _, property in data_schema["properties"].items():
            property.pop("title")
            if "enum" in property:
                property.pop("default")
        return data_schema
    
    def __call__(self, **fields):
        return self.__data_model(**fields)
