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
from swayam import Template
from .error import *

kallable = callable

def iterator(invoker, iterable):
    
    def validate_output(output):
        if not isinstance(output, Data):
            if output is None and invoker.allow_none_output:
                    return Template.NoneValue().as_dict()
            raise InjectableOutputNotAStructureError(invoker, output=output)
        elif not isinstance(output.model_instance, invoker.out_template.model):
            # The DataModel can be a sub-class of a parent model. This logic works when the parent model is set as the return type.
            raise InjectableInvalidOutputStructureError(invoker, output=output)

    for output in iterable:
        validate_output(output)
        yield output.as_dict()

class StructuredDriver(StructuredInjectableWithCallable):
    
    def __init__(self, name, *, callable, in_template, out_template, allow_none_output=False):
        if in_template is None:
            in_template = Template.Empty
        super().__init__(name, callable=callable, in_template=in_template, out_template=out_template, allow_none_output=allow_none_output)
        
    def validate_output(self, output):
        # In a generator, at this stage, it's to be checked where it is an iterable.
        try:
            iter(output)
            return True
        except TypeError:
            raise DriverCallableNotIterableError(self)
 
    def __call__(self, vault=None, **kwargs):
        class InjectableInvoker:
            def __init__(self, name, vault):
                self.name = name
                self.vault = vault
        output = self.call_encapsulated_callable(invoker=InjectableInvoker(name=self.name, vault=vault), **kwargs)
        return iterator(self, output)
