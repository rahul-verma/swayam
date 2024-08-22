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

class NumericOutputModel(BaseModel):
    output: Union[int, float] = Field(..., title="Numeric Output", description="A numeric output (int or float)")

class NumericListOutputModel(BaseModel):
    output: list[Union[int, float]] = Field(..., title="Numeric List Output", description="A numeric list output (int or float)")

class StringOutputModel(BaseModel):
    output: str = Field(..., title="String Output", description="A string output")

class StringListOutputModel(BaseModel):
    output: list[str] = Field(..., title="String List Output", description="A list of string outputs")

class BoolOutputModel(BaseModel):
    output: bool = Field(..., title="Boolean Output", description="A boolean output")

class BoolListOutputModel(BaseModel):
    output: list[bool] = Field(..., title="Boolean List Output", description="A list of boolean outputs")
    
NumericOutput, NumericOutputList = Structure.build("NumericOutput", model=NumericOutputModel, return_composite=True)
StringOutput, StringOutputList = Structure.build("StringOutput", model=StringOutputModel, return_composite=True)
BoolOutput, BoolOutputList = Structure.build("BoolOutput", model=BoolOutputModel, return_composite=True)