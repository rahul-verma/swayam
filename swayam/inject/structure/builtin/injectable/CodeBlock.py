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

from typing import List
from pydantic import BaseModel, Field

from swayam import Structure

class CodeBlockModel(BaseModel):
    code_block: str = Field(..., title="Text Content", description="Text Content of Code or Markdown or Plain text.")
    language: str = Field(default="markdown", title="Code Language", description="Language for the code block. E.g. python, javascript, etc. If not provided, it will be assumed to be plain text and type is set to markdown.")
    
class CodeBlocksModel(BaseModel):
    code_blocks: List[CodeBlockModel] = Field(..., title="Code Blocks", description="List of Code Blocks.")

CodeBlock = Structure.build("CodeBlock", model=CodeBlockModel)
CodeBlocks = Structure.build("CodeBlocks", model=CodeBlocksModel)