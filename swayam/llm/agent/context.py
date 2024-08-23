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

class AgentStore:
    
    def __init__(self):
        self.__storage = {}
        
    def reset(self):
        self.__storage = {}
        
    def __getitem__(self, key):
        return self.__storage[key]
    
    def __setitem__(self, key, value):
        self.__storage[key] = value
    
    def items(self):
        # Return an iterable of key-value pairs
        return self.__storage.items()
    
    def __iter__(self):
        # Iterator to allow unpacking
        return iter(self.__storage)
    

class AgentContext:
    
    def __init__(self):
        from swayam.llm.conversation.context import ConversationContext
        self.__conversation_context = ConversationContext()
        self.__store = AgentStore()
        
    @property
    def conversation_context(self):
        return self.__conversation_context
        
    def reset_conversation_context(self):
        self.__conversation_context.reset()
        
    def reset(self):
        self.__conversation_context.reset()
        self.__store.reset()
        
    @property
    def store(self):
        return self.__store
    
    def format_prompt(self, prompt):
        prompt.dynamic_format(self.store)
        
    