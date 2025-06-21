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
from swayam.inject.template.template import Data
from swayam.inject.error import *
from swayam import Template
from .error import *

# Define a base class `Structure` that inherits from `BaseModel`

kallable = callable

def iterator(invoker, driver):
    from swayam.inject.action.action import StructuredAction
    
    def validate_output(output):
        if not isinstance(output, Data):
            raise InjectableOutputNotAStructureError(invoker, output=output)
        elif not isinstance(output.model_instance, invoker.out_template.model):
            # The DataModel can be a sub-class of a parent model. This logic works when the parent model is set as the return type.
            raise InjectableInvalidOutputStructureError(invoker, output=output)

    # setup call
    try:
        output = next(driver)
        validate_output(output)
        yield output.as_dict()
    except Exception as e:
        import traceback
        raise PropSetUpError(invoker, error=str(e) + traceback.format_exc())
    
    # teardown call
    try:
        output = next(driver)
        validate_output(output)
        yield output.as_dict()
    except Exception as e:
        raise PropTearDownError(invoker, error=e)

class StructuredProp(StructuredInjectableWithCallable):
    
    def __init__(self, name, *, callable, in_template=None):
        if in_template is None:
            in_template = Template.Empty
        super().__init__(name, callable=callable, in_template=in_template, out_template=Template.Result)
        
    def validate_output(self, driver):
        # In a driver, at this stage, it's to be checked where it is an iterable.
        import inspect
        if not inspect.isdriver(driver):
            raise PropInvalidCallableError(self)
 
    def __call__(self, phase=None, **kwargs):
        # In direct injectable calling, the phase in none, hence no vault access if available. In the STEPs flow, the phase object is provided with vault access.
        class PropInvoker:
            def __init__(self, name, phase):
                self.name = name
                self.__phase = phase
                
            @property
            def vault(self):
                return self.__phase.vault
            
        driver = self.call_encapsulated_callable(
            invoker=PropInvoker(self.name, phase),
            **kwargs)
        return iterator(self, driver)
