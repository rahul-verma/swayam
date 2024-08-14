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



import json

class Tool:
    
    def __init__(self, target, desc, tool_structure):
        self.__name = target.__name__
        self.__target = target
        self.__desc = desc
        self.__tool_structure = tool_structure
        
    @property
    def name(self):
        return self.__name
    
    @property
    def qname(self):
        return self.__target.__module__ + "." + self.__name
    
    @property
    def desc(self):
        return self.__desc
    
    @property
    def definition(self):
        data_schema = json.loads(self.__tool_structure.schema_json())
        data_schema.pop("title")
        for _, property in data_schema["properties"].items():
            if "enum" in property:
                property.pop("title")
                property.pop("default")
        schema = {
            "type": "function",
            "function":{
                "name": self.__name,
                "description": self.__desc,
                "parameters": data_schema
            }}
        return schema
    
    def __call__(self, **fields):
        structure = self.__tool_structure(**fields)
        return self.__target(**structure.dict())

    @classmethod
    def structure_builder(cls, name:str):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the structure
        """
        from .structure import StructureBuilder
        return StructureBuilder(name)
    
    @classmethod
    def tool_builder(cls, target, desc:str=None, **fields):
        from .builder import ToolBuilder
        return ToolBuilder(target, desc, **fields)
    
    
