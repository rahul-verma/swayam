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
from swayam.inject.error import *
from swayam import Structure
from .error import *

# Define a base class `Structure` that inherits from `BaseModel`

kallable = callable

def iterator(invoker, generator):
    from swayam.inject.tool.tool import StructuredTool
    
    def validate_output(output):
        if not isinstance(output, IOStructureObject):
            raise InjectableOutputNotAStructureError(invoker, output=output)
        elif not isinstance(output.model_instance, invoker.output_structure.data_model):
            # The DataModel can be a sub-class of a parent model. This logic works when the parent model is set as the return type.
            raise InjectableInvalidOutputStructureError(invoker, output=output)

    # setup call
    try:
        output = next(generator)
        validate_output(output)
        yield output.as_dict()
    except Exception as e:
        import traceback
        raise ResourceSetUpError(invoker, error=str(e) + traceback.format_exc())
    
    # teardown call
    try:
        output = next(generator)
        validate_output(output)
        yield output.as_dict()
    except Exception as e:
        raise ResourceTearDownError(invoker, error=e)

class StructuredResource(StructuredInjectableWithCallable):
    
    def __init__(self, name, *, callable, input_structure=None):
        if input_structure is None:
            input_structure = Structure.Empty
        super().__init__(name, callable=callable, input_structure=input_structure, output_structure=Structure.Result)
        
    def validate_output(self, generator):
        # In a generator, at this stage, it's to be checked where it is an iterable.
        import inspect
        if not inspect.isgenerator(generator):
            raise ResourceInvalidCallableError(self)
 
    def __call__(self, phase, **kwargs):
        class ResourceInvoker:
            def __init__(self, name, phase):
                self.name = name
                self.__phase = phase
                
            @property
            def store(self):
                return self.__phase.store
            
        generator = self.call_encapsulated_callable(
            invoker=ResourceInvoker(self.name, phase),
            **kwargs)
        return iterator(self, generator)
