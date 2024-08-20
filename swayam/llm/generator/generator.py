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


def iterator(data_object, output_structure):
    for data in data_object:
        yield output_structure(**data).dict()

class MapGenerator:
    
    def __init__(self, name, *, data_object, output_structure):
        self.__name = name
        self.__data_object = data_object
        self.__output_structure = output_structure
 
    def __iter__(self):
        return iterator(self.__data_object, self.__output_structure)
