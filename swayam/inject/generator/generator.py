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
from swayam.inject.structure.structure import IOStructureObject
from swayam.inject.error import InjectableInvalidOutputError
from swayam import Structure
from .error import *

# Define a base class `Structure` that inherits from `BaseModel`

kallable = callable

def iterator(caller, iterable):
    from swayam.inject.tool.tool import StructuredTool
    
    def validate_output(output):
        from swayam.inject.error import InjectableInvalidOutputError
        from swayam import Structure
        if not isinstance(output, IOStructureObject):
            if output is None and caller.allow_none_output:
                    return Structure.NoneValue().as_dict()
            raise InjectableInvalidOutputError(caller, output=output)
        elif not isinstance(output.model_instance, caller.output_structure.data_model):
            # The DataModel can be a sub-class of a parent model. This logic works when the parent model is set as the return type.
            raise InjectableInvalidOutputError(caller, output=output.name)

    for output in iterable:
        validate_output(output)
        yield output.as_dict()

class StructuredGenerator(StructuredInjectableWithCallable):
    
    def __init__(self, name, *, callable, input_structure, output_structure, allow_none_output=False):
        if input_structure is None:
            input_structure = Structure.Empty
        super().__init__(name, callable=callable, input_structure=input_structure, output_structure=output_structure, allow_none_output=allow_none_output)
        
    def validate_output(self, output):
        # In a generator, at this stage, it's to be checked where it is an iterable.
        try:
            iter(output)
            return True
        except TypeError:
            raise GeneratorCallableNotIterableError(self)
 
    def __call__(self, **kwargs):
        output = self.call_encapsulated_callable(**kwargs)
        return iterator(self, output)
