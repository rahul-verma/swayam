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

from swayam.core.store import Store

class AgentContext:
    
    def __init__(self):
        from swayam.llm.action.context import ActionContext
        self.__action_context = ActionContext()
        self.__store = Store()
        
    @property
    def action_context(self):
        return self.__action_context
        
    def reset_action_context(self):
        self.__action_context.reset()
        
    def reset(self):
        self.__action_context.reset()
        self.__store.reset()
        
    @property
    def store(self):
        return self.__store
    
    def format_request(self, request):
        request.dynamic_format(self.store)
        
    