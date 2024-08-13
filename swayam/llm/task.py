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
from .prompt.prompt import Prompt
from .prompt.converse import Conversation
from .prompt.context import PromptContext

class Task:
    """
    Represents a sequence of conversations, commonly in the same context.
    """
    
    def __init__(self, *conversations, same_context=True):
        if not conversations:
            self.__conversations = []
        else:
            self.__conversations = []
            for conversation in conversations:
                self.append(conversation)
        self.__same_context = same_context
        self.__context = PromptContext()
        
    def append(self, node):
        message = Conversation.load_message(node)._get_first_child()
        if isinstance (message, Prompt):
            message = Conversation(message)
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
        