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
from swayam.llm.prompt import Prompt
from swayam.llm.prompt.converse import Conversation
from swayam.llm.prompt.context import PromptContext

class Task:
    """
    Represents a sequence of conversations, commonly in the same context.
    """
    
    def __init__(self, *conversations, system_prompt=None, same_context=True):
        self.__conversations = []
        self.__system_prompt = system_prompt
        self.__same_context = same_context
        if conversations:
            for conversation in conversations:
                self.append(conversation)
        self.__context = PromptContext()
        
    def append(self, node):
        message = None
        if isinstance(node, Conversation):
            message = node
        else:
            message = Conversation.load_message(node)._get_first_child()
        if isinstance (message, Prompt):
            message = Conversation(message)
        # First node
        if self.__same_context and len(self.__conversations) == 0:
            message.append_system_prompt(self.__system_prompt) 
        if not self.__same_context:
            message.append_system_prompt(self.__system_prompt)
        self.__conversations.append(message)

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            if not self.__same_context:
                self.__context = PromptContext()
            conversation = self.__conversations[self.__index]
            conversation.context = self.__context
            log_debug("Context Length: ", len(self.__context.messages))
            return conversation
        except IndexError:
            self.__index = -1
            raise StopIteration()
        

        
    
        context = PromptContext()
        