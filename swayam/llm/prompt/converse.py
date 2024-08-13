
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

from tarkash import log_debug
from .prompt import *
from .context import PromptContext

class Conversation:
    
    def __init__(self, *prompts:Prompt) -> Any:
        self.__prompts = list(prompts)
        self.__context = None
        
    def append(self, prompt:Prompt):
        self.__prompts.append(prompt)
        
    @property
    def context(self):
        return self.__context
    
    @context.setter
    def context(self, context:PromptContext):
        self.__context = context
        
    def __len__(self):
        return len(self.__prompts)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Conversation.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Conversation (Length: {len(self)})\n"
        
        for prompt in self.__prompts:
            if isinstance(prompt, Conversation):
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
    
    @classmethod
    def load_message(cls, input_object, sequence=None, **kwargs):
        log_debug("Loading Prompt object")
        log_debug(f"Input: {type(input_object)}, Sequence: {sequence}")
        if sequence is None:
            sequence = Conversation()

        from swayam.llm.prompt.file import PromptTextFile, PromptIniFile
        if isinstance(input_object, PromptTextFile) :
            return cls.load_message(input_object.content, sequence, **kwargs)
        elif isinstance(input_object, PromptIniFile):
            sub_sequence = Conversation()
            for value in input_object.content.values():
                cls.load_message(value, sub_sequence, **kwargs)
            sequence.append(sub_sequence)
            return sequence
        elif isinstance(input_object, list):
            sub_sequence = Conversation()
            for item in input_object:
                cls.load_message(item, sub_sequence, **kwargs)
            sequence.append(sub_sequence)
            return sequence
        elif isinstance(input_object, dict):
            if input_object["role"] == "system":
                sequence.append(SystemPrompt(input_object["content"], **kwargs))
            elif input_object["role"] == "user":
                sequence.append(UserPrompt(input_object["content"], **kwargs))
            else:
                raise TypeError(f"Invalid PromptNode type: {type(input_object)}")
        elif isinstance(input_object, str):
            if input_object.lower().endswith('.txt'):
                return cls.load_message(PromptTextFile(input_object).content, sequence, **kwargs)
            elif input_object.lower().endswith('.ini'):
                return cls.load_message(list(PromptIniFile(input_object).content.values()), sequence, **kwargs)
            else:
                sequence.append(UserPrompt(input_object, **kwargs))
        elif isinstance(input_object, Prompt):
            sequence.append(input_object)
        elif isinstance(input_object, Conversation):
            sequence.append(input_object)
        else:
            raise TypeError(f"Invalid PromptNode type: {type(input_object)}")
        
        log_debug(f"Returning: Sequence: {sequence}")
        return sequence