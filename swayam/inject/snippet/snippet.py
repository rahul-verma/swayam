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

from enum import Enum
from swayam.inject.template import Template
from swayam.inject.template.template import Data

kallable = callable

class StructuredSnippet:
    
    def __init__(self, *, purpose, text):
        self.__purpose = purpose
        self.__text = text
        
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def text(self):
        return self.__text
 
    def __call__(self, **kwargs):
        args = self.__in_template(**kwargs).as_dict()
        output = self.__callable(**args)
        
        if isinstance(output, Data):
            output = output.as_dict()
        else:
            if self.__out_template.is_atomic():
                output = self.__out_template(**output).as_dict()
            else:
                output = self.__out_template(**output).as_list()
        
        self.prompt.append_output(output)        