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

from swayam.inject.injectable import StructuredInjectable

class StructuredTool(StructuredInjectable):
    
    def __init__(self, name, *, callable, description, input_structure, output_structure):
        super().__init__(name, input_structure=input_structure, output_structure=output_structure)
        self.__callable = callable
        self.__callable_name = self.__callable.__name__
        self.__description = description
        from swayam.inject import Injectable
        Injectable.validate_callable_definition(self)
    
    @property
    def callable_name(self):
        return self.__callable_name
    
    @property
    def callable(self):
        return self.__callable
    
    @property
    def description(self):
        return self.__description
    
    @property
    def definition(self):
        data_schema = self.input_structure.definition
        schema = {
            "type": "function",
            "function":{
                "name": self.name,
                "description": self.description,
                "parameters": data_schema
            }}
        return schema
    
    def __call__(self, **kwargs):
        from swayam.inject import Injectable
        return Injectable.call(self, **kwargs)