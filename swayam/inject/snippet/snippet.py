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
from swayam.inject.structure import Structure
from swayam.inject.structure.structure import IOStructureObject

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
        from swayam.inject.tool.tool import StructuredTool
    
        output_iterable = None

        args = self.__input_structure(**kwargs).as_dict()
        output = self.__callable(**args)
        
        if isinstance(output, IOStructureObject):
            output = output.as_dict()
        else:
            if self.__output_structure.is_atomic():
                output = self.__output_structure(**output).as_dict()
            else:
                output = self.__output_structure(**output).as_list()
        
        self.prompt.append_output(output)

        
class StructuredSnippetCreator:
    
    def __init__(self, name, *, callable):
        self.__name = name
        
        if not kallable(callable):
            raise SnippetArgIsNotCallableError(self.__name, callable=callable)
        self.__callable = callable

    def __call__(self):
        output = self.__callable(caller=self)
        if not isinstance(output, IOStructureObject):
            raise SnippetCallableOutputError(self.__name, actual_object=output)
        elif output.struct_name != "Snippet":
            raise SnippetCallableOutputError(self.__name, actual_name=output.name)
        else:
            return StructuredSnippet(**output.as_dict())
        
        