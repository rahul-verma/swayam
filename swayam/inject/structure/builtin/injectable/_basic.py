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

class NumericValueModel(BaseModel):
    value: Union[int, float] = Field(..., title="Numeric Content", description="A numeric content (int or float)")
    
class CounterModel(BaseModel):
    counter: int = Field(..., title="Integer Counter", description="Integer value counter")
    
class NumericValuesModel(BaseModel):
    values: list[Union[int, float]] = Field(..., title="Numeric List Content", description="A list of numeric contents (int or float)")

class StringValueModel(BaseModel):
    value: str = Field(..., title="String content", description="A string content")

class StringValuesModel(BaseModel):
    values: list[str] = Field(..., title="String List Content", description="A list of string contents")

class BoolValueModel(BaseModel):
    value: bool = Field(..., title="Boolean Content", description="A boolean content")

class BoolValuesModel(BaseModel):
    values: list[bool] = Field(..., title="Boolean List Content", description="A list of boolean contents")
    
class NoneValueModel(BaseModel):
    value: None = Field(None, title="None Content", description="A None content")
    
NumericValue = Structure.build("NumericValue", model=NumericValueModel)
Counter = Structure.build("Counter", model=CounterModel)
NumericValues = Structure.build("NumericValues", model=NumericValuesModel)
StringValue = Structure.build("StringValue", model=StringValueModel)
StringValues = Structure.build("StringValues", model=StringValuesModel)
BoolValue = Structure.build("BoolValue", model=BoolValueModel)
BoolValues = Structure.build("BoolValues", model=BoolValuesModel)
NoneValue = Structure.build("NoneValue", model=NoneValueModel)