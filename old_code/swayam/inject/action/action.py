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

from swayam.inject.injectable import StructuredInjectableWithCallable

class StructuredAction(StructuredInjectableWithCallable):
    
    def __init__(self, name, *, callable, description, in_template=None, out_template=None, allow_none_output=False):
        from swayam import Template
        if in_template is None:
            in_template = Template.Empty
        if out_template is None:
            out_template = Template.Empty
        super().__init__(name, callable=callable, in_template=in_template, out_template=out_template, allow_none_output=allow_none_output)
        self.__description = description
        
    @property
    def description(self):
        return self.__description
    
    @property
    def definition(self):
        data_schema = self.in_template.definition
        schema = {
            "type": "function",
            "function":{
                "name": self.name,
                "description": self.description,
                "parameters": data_schema
            }}
        return schema