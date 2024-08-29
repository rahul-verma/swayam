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

from typing import Union
from pydantic import BaseModel, Field

from swayam import Structure

class NumericModel(BaseModel):
    content: Union[int, float] = Field(..., title="Numeric Content", description="A numeric content (int or float)")
    
class NumericsModel(BaseModel):
    content: list[Union[int, float]] = Field(..., title="Numeric List Content", description="A list of numeric contents (int or float)")

class StringModel(BaseModel):
    content: str = Field(..., title="String content", description="A string content")

class StringsModel(BaseModel):
    content: list[str] = Field(..., title="String List Content", description="A list of string contents")

class BoolModel(BaseModel):
    content: bool = Field(..., title="Boolean Content", description="A boolean content")

class BoolsModel(BaseModel):
    content: list[bool] = Field(..., title="Boolean List Content", description="A list of boolean contents")
    
class NullModel(BaseModel):
    content: None = Field(None, title="None Content", description="A None content")
    
Numeric = Structure.build("Numeric", model=NumericModel)
Numerics = Structure.build("Numerics", model=NumericsModel)
String = Structure.build("String", model=StringModel)
Strings = Structure.build("Strings", model=StringsModel)
Bool = Structure.build("Bool", model=BoolModel)
Bools = Structure.build("Bools", model=BoolsModel)
Null = Structure.build("Null", model=NullModel)