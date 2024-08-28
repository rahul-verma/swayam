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

from typing import Union, List
from pydantic import BaseModel, Field

from swayam import Structure

class ContentCodeBlockFilterModel(BaseModel):
    input_content: str = Field(..., title="Text Content", description="Source text content to be parsed")
    languages: List[str] = Field(default=None, title="Language names for filtering", description="Language for filtering the code blocks in text. E.g. python, javascript, etc. If not provided, it will be assumed to be plain text and type is set to markdown.")
    strict: bool = Field(True, title="Strict Match", description="If True, raise an error if no code block is found in the content")

ContentCodeBlockFilter = Structure.build("ContentCodeBlockFilter", model=ContentCodeBlockFilterModel)