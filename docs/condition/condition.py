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

from swayam.inject.error import *
from swayam import Structure

class StructuredCondition:
    
    def __init__(self, name, *, callable):
        self.__name = name
        self.__callable = callable
        self.__store = None
        
    @property
    def output_structure(self):
        return Structure.Boolean
        
    @property
    def store(self):
        return self.__store
    
    @store.setter
    def store(self, store):
        self.__store = store
 
    def __call__(self, **kwargs):
        from swayam.inject.tool.tool import StructuredTool
        
        output = self.__callable(condition=self, **kwargs)
        
        if not isinstance(output, bool):
            raise InjectableInvalidOutputError(self, output=output)
    
        return {'output': output}

        
