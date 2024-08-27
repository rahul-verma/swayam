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
import re
import json

from swayam import Parser
from swayam.inject.structure import Structure

def extract_code_blocks(*, parser, content:str, languages:List[str]=None, strict=True) -> str:
    """
    Extracts code blocks from an LLM response, supporting both Markdown and JSON.
    
    Args:
        content (str): The response from the LLM containing code blocks.
    """
    # Regular expression to find code blocks with optional language info
    code_block_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
    
    if languages is not None:
        languages = [language.strip().lower() for language in languages]
            
    # Find all matches
    code_blocks = code_block_pattern.findall(content)
    
    extracted_content = []
    
    for found_language, content in code_blocks:
        content = content.strip()
        # Default to markdown if no language is specified
        found_language = found_language.strip().lower() if found_language else "markdown"
        
        if languages is not None:
            if found_language not in languages:
                continue

        if found_language:
            extracted_content.append({"language": found_language, "content": content})
        else:
            extracted_content.append({"content": content})
    
    from swayam.inject.parser.error import ParserNoMatchError
    if strict and not extracted_content:
        raise ParserNoMatchError(parser.name, f"No Code block was found in for languages {languages} in the following content:\n>>{content}<<.")
    return extracted_content

CodeBlockExtractor = Parser.text(
    "CodeBlockExtractor",
    kallable=extract_code_blocks,
    input_structure=Structure.ContentCodeBlockFilter,
    output_structure=Structure.CodeBlockList
)