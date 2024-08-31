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
from swayam import Structure
from .error import *

class StructuredParser(StructuredInjectableWithCallable):
    
    def __init__(self, name, *, callable, input_structure, output_structure, allow_none_output=False):
        super().__init__(name, callable=callable, input_structure=input_structure, output_structure=output_structure, allow_none_output=allow_none_output)
    
class TextContentParser(StructuredParser):
    
    def __init__(self, name, *, callable, input_structure=None, output_structure=None, allow_none_output=False):
        from swayam.inject.structure.builtin import TextContent
        if input_structure is None:
            input_structure = Structure.TextContent
        elif not issubclass(input_structure.data_model, Structure.TextContent.data_model):
            raise TextParserIncompatibleInputStructureError(self)
        else:
            input_structure = input_structure
        if output_structure is None:
            output_structure = Structure.StringValues
        super().__init__(name, callable=callable, input_structure=input_structure, output_structure=output_structure, allow_none_output=allow_none_output)
        
class JsonContentParser(StructuredParser):
    
    def __init__(self, name, *, callable, output_structure, input_structure=None,      content_structure=None, allow_none_output=False):
        from swayam.inject.structure.builtin import TextContent
        if input_structure is None:
            input_structure = Structure.JsonContent
        elif not issubclass(input_structure.data_model, Structure.JsonContent.data_model):
            raise JsonParserIncompatibleInputStructureError(self)
        super().__init__(name, callable=callable, input_structure=input_structure, output_structure=output_structure, allow_none_output=allow_none_output)
        self.__content_structure = content_structure
        
    @property
    def content_structure(self):
        return self.__content_structure
    
    def validate_input_content(self, **kwargs):
        content = kwargs["content"]
        if self.__content_structure:
            self.__content_structure(**content)
    
    