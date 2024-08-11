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

from typing import Any
from tarkash import log_info

class Prompt:
    
    def __init__(self, *, role, content) -> Any:
        self.__message = {
            "role": role,
            "content": content
        }
        
    @property
    def message(self):
        return self.__message
    
    @classmethod
    def load_prompt_object(cls, input_object, sequence=None):
        log_info("Loading Prompt object")
        log_info(f"Input: {type(input_object)}, Sequence: {sequence}")
        if sequence is None:
            sequence = PromptSequence()

        from swayam.llm.prompt.file import PromptTextFile, PromptIniFile
        if isinstance(input_object, PromptTextFile) :
            return Prompt.load_prompt_object(input_object.content, sequence)
        elif isinstance(input_object, PromptIniFile):
            return Prompt.load_prompt_object(input_object.content.values(), sequence)
        elif isinstance(input_object, list):
            for item in input_object:
                return Prompt.load_prompt_object(item, sequence)
        elif isinstance(input_object, dict):
            if input_object["role"] == "system":
                sequence.append(SystemPrompt(input_object["content"]))
            elif input_object["role"] == "user":
                sequence.append(UserPrompt(input_object["content"]))
            elif input_object["role"] == "function":
                sequence.append(FunctionPrompt(input_object["content"]))
            elif input_object["role"] == "tool":
                sequence.append(ToolPrompt(input_object["content"]))
            else:
                raise TypeError(f"Invalid PromptNode type: {type(input_object)}")
        elif isinstance(input_object, str):
            if input_object.lower().endswith('.txt'):
                return Prompt.load_prompt_object(PromptTextFile(input_object).content, sequence)
            elif input_object.lower().endswith('.ini'):
                return Prompt.load_prompt_object(PromptIniFile(input_object).content.values(), sequence)
            else:
                sequence.append(UserPrompt(input_object))
        else:
            raise TypeError(f"Invalid PromptNode type: {type(input_object)}")
        
        log_info(f"Returning: Sequence: {sequence}")
        return sequence

class SystemPrompt(Prompt):
    
    def __init__(self, content:str) -> Any:
        super().__init__(role="system", content=content)

class UserPrompt(Prompt):
    def __init__(self, content:str) -> Any:
        super().__init__(role="system", content=content)

class FunctionPrompt(Prompt):
    def __init__(self, content:str) -> Any:
        super().__init__(role="function", content=content) # !!!!! Not sure

class ToolPrompt(Prompt):
    def __init__(self, content:str) -> Any:
        super().__init__(role="tool", content=content)  # !!!!! Not sure

class PromptSequence:
    
    def __init__(self, *prompts:Prompt) -> Any:
        self.__prompts = list(prompts)
        
    def append(self, prompt:Prompt):
        self.__prompts.append(prompt)
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__prompts[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()