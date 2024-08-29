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

kallable = callable

import inspect
from .error import *
from swayam.inject import Injectable
from swayam import Structure
class StructuredInjectable:
    
    def __init__(self, name, *, input_structure, output_structure):
        self.__type = self.__class__.__name__
        self.__name = name
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        
    @property
    def type(self):
        return self.__type
    
    @property
    def name(self):
        return self.__name
    
    @property
    def input_structure(self):
        return self.__input_structure
    
    @property
    def output_structure(self):
        return self.__output_structure
    
    @property
    def allowed_keywords(self):
        from_data_model = list(self.__input_structure.keys)
        from_data_model.insert(0, "caller")
        return from_data_model
    
class StructuredInjectableWithCallable(StructuredInjectable):
    
    def __init__(self, name, *, callable, input_structure, output_structure, allow_none_output=False):
        super().__init__(name, input_structure=input_structure, output_structure=output_structure)
        self.__callable = callable
        self.__allow_none_output = allow_none_output
        self.__validate_callable_definition()

    @property
    def callable(self):
        return self.__callable
    @property
    def allow_none_output(self):
        return self.__allow_none_output

    def __validate_callable_definition(self):
        # Check if it is a callable
        if not kallable(self.callable):
            raise InjectableNotCallableError(self)
        
        # Get the signature of the function
        signature = inspect.signature(self.callable)
        
        for param in signature.parameters.values():
            if param.kind != inspect.Parameter.KEYWORD_ONLY:
                raise InjectableInvalidCallableDefinitionError(self, error="Found non-keyword arguments in definition.")
            
        # Extract keyword-only arguments
        keyword_only_params = [
            param for param in signature.parameters.values()
            if param.kind == inspect.Parameter.KEYWORD_ONLY
        ]
        
        # Get the names of these parameters
        keyword_only_names = {param.name for param in keyword_only_params}
        
        # Check if all parameters are keyword-only and match the expected names
        if not keyword_only_names == set(self.allowed_keywords):
            raise InjectableInvalidCallableDefinitionError(self, error=f"Found {keyword_only_names} in definition.")
    def __call__(self, **kwargs):
        from swayam.inject.structure.structure import IOStructureObject
        try:
            output = self.callable(caller=self, **kwargs)
        except Exception as e:
            import traceback
            frame = traceback.extract_tb(e.__traceback__)[-1]
            frame_str = Injectable.extract_caller_from_frame(frame)
            raise InjectableCallError(self, error=str(e) + f". Check: {frame_str}")
        else:      
            if not isinstance(output, IOStructureObject):
                if output is None and self.allow_none_output:
                    return Structure.Null().as_dict()
                raise InjectableInvalidOutputError(self, output=output)
            elif not isinstance(output.model_instance, self.output_structure.data_model):
                # The DataModel can be a sub-class of a parent model. This logic works when the parent model is set as the return type.
                raise InjectableInvalidOutputError(self, output=output.name)
            else:
                return output.as_dict()