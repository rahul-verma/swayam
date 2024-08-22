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

class NumericResultModel(BaseModel):
    result: Union[int, float] = Field(..., title="Numeric Result", description="A numeric result (int or float)")

class NumericListResultModel(BaseModel):
    result: list[Union[int, float]] = Field(..., title="Numeric List Result", description="A numeric list result (int or float)")

class StringResultModel(BaseModel):
    result: str = Field(..., title="String Result", description="A string result")

class StringListResultModel(BaseModel):
    result: list[str] = Field(..., title="String List Result", description="A list of string results")

class BoolResultModel(BaseModel):
    result: bool = Field(..., title="Boolean Result", description="A boolean result")

class BoolListResultModel(BaseModel):
    result: list[bool] = Field(..., title="Boolean List Result", description="A list of boolean results")
    
NumericResult = Structure.build("NumericResult", model=NumericResultModel)
NumericListResult = Structure.build("NumericListResult", model=NumericListResultModel)
StringResult = Structure.build("StringResult", model=StringResultModel)
StringListResult = Structure.build("StringListResult", model=StringListResultModel)
BoolResult = Structure.build("BoolResult", model=BoolResultModel)
BoolListResult = Structure.build("BoolListResult", model=BoolListResultModel)