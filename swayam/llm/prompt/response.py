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

class LLMResponse:
    
    def __init__(self, message, *, error=False) -> None:
        self.__message = message
        self.__error = error
        if error:
            self.__content = self.__message["content"]
        else:
            self.__content = self.__message.content
        
        
    @property
    def message(self):
        return self.__message
    
    @property
    def content(self):
        return self.__content
    
    @property
    def error(self):
        return self.__error
    
    def as_dict(self) -> dict:
        if self.__error:
            return self.__message
        else:
            return self.__message.to_dict()
        
        
class ToolResponse:
    
    def __init__(self, *, tool_id, tool_name, content):
        self.__tool_id = tool_id
        self.__tool_name = tool_name
        self.__content = content
        
    @property
    def tool_id(self):
        return self.__tool_id
    
    @property
    def tool_name(self):
        return self.__tool_name
    
    @property
    def content(self):
        return self.__content