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

class ToolResponse:
    
    def __init__(self, tool, result):
        self.__tool = tool
        self.__tool_name = tool.name
        self.__tool_definition = tool.definition
        self.__result = result
        self.__tool_id = None
    
    @property
    def tool_id(self):
        return self.__tool_id
    
    @tool_id.setter
    def tool_id(self, value):
        self.__tool_id = value    
        
    @property
    def tool(self):
        return self.__tool
    
    @property
    def tool_name(self):
        return self.__tool.name
    
    @property
    def definition(self):
        return self.__tool_definition
    
    @property
    def content(self):
        return self.__result