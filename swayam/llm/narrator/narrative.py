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

from swayam.core.store import STEPStore

class Narrative:
    
    def __init__(self):
        from swayam.llm.expression.conversation import Conversation
        self.__conversation = Conversation()
        self.__store = STEPStore()
        self.__directive = ""
        
    @property
    def conversation(self):
        return self.__conversation
        
    def reset_conversation(self):
        self.__conversation.reset()
        
    def reset(self):
        self.reset_conversation()
        self.store.reset()
        
    @property
    def store(self):
        return self.__store
    
    def format_prompt(self, prompt):
        prompt.dynamic_format(self.store)
        
    def add_directive(self, directive):
        self.__directive += directive + "\n\n"
    @property
    def directive(self):
        return self.__directive
        
    