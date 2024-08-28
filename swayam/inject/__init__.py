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

import inspect
import importlib
from .error import *

kallable = callable

class Injectable:
    
    @classmethod
    def load_module(cls, type, name):
        
        class InjectableClass:
            def __init__(self, type, name, module_name):
                self.__type = type.lower().title()
                self.__name = name
                self.__module_name = module_name
            
            @property
            def type(self):
                return self.__type
            
            @property
            def name(self):
                return self.__name
            
            @property
            def module_name(self):
                return self.__module_name
    
        type = type.lower()
        from tarkash import Tarkash, TarkashOption
        project_name = Tarkash.get_option_value(TarkashOption.PROJECT_NAME)
            
        module_name = f"{project_name}.lib.inject.{type.lower()}"
        try:
            injectable_module = importlib.import_module(module_name)
            return getattr(injectable_module, name)
        except InjectableObjectError as e:
            this_object = InjectableClass(type, module_name=module_name, name=name)
            raise InjectableNameImportError(this_object, error=str(e))
        except (ModuleNotFoundError, AttributeError) as e:
            pass
        
        module_name = f"swayam.inject.{type.lower()}.builtin"
        try:
            injectable_module = importlib.import_module(module_name)
            return getattr(injectable_module, name)
        except InjectableObjectError as e:
            this_object = InjectableClass(type, module_name=module_name, name=name)
            raise InjectableNameImportError(this_object, error=str(e))
        except AttributeError as e:
            pass
        
        raise InjectableNameNotFoundError(InjectableClass(type, module_name=None, name=name))
    
    @classmethod
    def validate_callable_definition(cls, injectable):
        # Check if it is a callable
        if not kallable(injectable.callable):
            raise InjectableNotCallableError(injectable)
        
        # Get the signature of the function
        signature = inspect.signature(injectable.callable)
        
        # Extract keyword-only arguments
        keyword_only_params = [
            param for param in signature.parameters.values()
            if param.kind == inspect.Parameter.KEYWORD_ONLY
        ]
        
        # Get the names of these parameters
        keyword_only_names = {param.name for param in keyword_only_params}
        
        # Check if all parameters are keyword-only and match the expected names
        if not keyword_only_names == set(injectable.allowed_keywords):
            raise 
        
    @classmethod
    def call(cls, injectable, **kwargs):
        try:
            return injectable.callable(caller=injectable, **kwargs)
        except Exception as e:
            raise InjectableCallError(injectable, error=e)
        