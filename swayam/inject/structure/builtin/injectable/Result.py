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

from typing import Generic, TypeVar, Union, Literal
from pydantic import BaseModel, Field

from swayam import Structure

ResultLiteral = TypeVar('ResultLiteral', Literal['success'], Literal['error'], Literal['failure'])

# Create the generic ResultModel
class ResultModel(BaseModel, Generic[ResultLiteral]):
    result: ResultLiteral = Field(..., title="Result", description="A message indicating the type of result.")
    message: str = Field(..., title="Message", description="A message describing the result.")

# SuccessModel inherits from ResultModel with the result literal set to "success"
class SuccessModel(ResultModel[Literal["success"]]):
    result: Literal["success"] = Field("success", title="Successful Response", description="Indicates a successful activity.")
    message: str = Field("The activity was successful", title="Message", description="A message describing the result.")

class FailureModel(ResultModel[Literal["error"]]):
    result: Literal["failure"] = Field("failure", title="Failure Response", description="Indicates an failed activity.")
    
# ErrorModel inherits from ResultModel with the result literal set to "error"
class ErrorModel(ResultModel[Literal["error"]]):
    result: Literal["error"] = Field("error", title="Error Response", description="Indicates an error in activity.")

Result = Structure.build("Result", model=ResultModel)    
Success = Structure.build("Success", model=SuccessModel)
Failure = Structure.build("Failure", model=FailureModel)
Error = Structure.build("Error", model=ErrorModel)