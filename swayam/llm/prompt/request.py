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

from copy import deepcopy
from typing import Any
from tarkash import log_debug
from tarkash import ImageFile

class Prompt:
    
    def __init__(self, *, role, content, image=None) -> Any:
        if image is None:
            self.__message = {
                "role": role,
                "content": content
            }
            self.__reportable_message = self.__message
        else:
            self.__image_path = image.full_path
            self.__image = image
            self.__message = {"role": "user", "content": [
                                {"type": "text", "text": content},
                                {"type": "image_url", "image_url": {"url": image.as_data_url}}
                            ]}
            self.__reportable_message = deepcopy(self.__message)
            temp_content = self.__reportable_message["content"]
            self.__reportable_text = temp_content
            if type(temp_content) == list:
                for item in temp_content:
                    if item["type"] == "text":
                        self.__reportable_text = item["text"]
                    elif item["type"] == "image_url":
                        prefix = self.__image.as_data_url.split(",")[0]
                        item["description"] = f"{prefix}, <Base64 encoded content of {self.__image_path}>."
                        item["local_path"] = self.__image_path
                        del item["image_url"]
        
    @property
    def message(self):
        return self.__message
    
    @property
    def content(self):
        return self.__message["content"]
    
    @property
    def role(self):
        return self.__message["role"]
    
    @property
    def image_path(self):
        return self.__image_path
    
    @property
    def reportable_text(self):
        return self.__reportable_text
    
    @property
    def reportable_content(self):
        return self.__reportable_message["content"]
    
    @property
    def reportable_message(self):
        return self.__reportable_message   
    
    @classmethod
    def load_prompt_object(cls, input_object, sequence=None):
        log_debug("Loading Prompt object")
        log_debug(f"Input: {type(input_object)}, Sequence: {sequence}")
        if sequence is None:
            sequence = PromptSequence()

        from swayam.llm.prompt.file import PromptTextFile, PromptIniFile
        if isinstance(input_object, PromptTextFile) :
            return cls.load_prompt_object(input_object.content, sequence)
        elif isinstance(input_object, PromptIniFile):
            sub_sequence = PromptSequence()
            for value in input_object.content.values():
                cls.load_prompt_object(value, sub_sequence)
            sequence.append(sub_sequence)
            return sequence
        elif isinstance(input_object, list):
            sub_sequence = PromptSequence()
            for item in input_object:
                cls.load_prompt_object(item, sub_sequence)
            sequence.append(sub_sequence)
            return sequence
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
                return Prompt.load_prompt_object(list(PromptIniFile(input_object).content.values()), sequence)
            else:
                sequence.append(UserPrompt(input_object))
        elif isinstance(input_object, Prompt):
            sequence.append(input_object)
        else:
            raise TypeError(f"Invalid PromptNode type: {type(input_object)}")
        
        log_debug(f"Returning: Sequence: {sequence}")
        return sequence

class SystemPrompt(Prompt):
    
    def __init__(self, content:str) -> Any:
        super().__init__(role="system", content=content)

class UserPrompt(Prompt):
    def __init__(self, content:str, image:str=None) -> Any:
        image = ImageFile(image) if image else None
        super().__init__(role="user", content=content, image=image)
        
    @property
    def image(self):
        return self.__image
    
    @property
    def image_as_data_url(self):
        return self.__image.as_data_url if self.__image else None

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
        
    def __len__(self):
        return len(self.__prompts)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the PromptSequence.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}PromptSequence (Length: {len(self)})\n"
        
        for prompt in self.__prompts:
            if isinstance(prompt, PromptSequence):
                description += prompt.describe(level + 1)
            else:
                description += f"{indent}  {type(prompt).__name__}\n"
        
        return description
        
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
        
    def _get_first_child(self):
        return self.__prompts[0]