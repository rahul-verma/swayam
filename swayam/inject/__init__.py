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
    def load_module(cls, type, name, caller_file=None):
    
        type = type.lower()
        from tarkash import Tarkash, TarkashOption
        project_name = Tarkash.get_option_value(TarkashOption.PROJECT_NAME)
        
        def raise_import_exception(e):
            this_object = cls.create_metadata_object(type=type, name=name, module_name=module_name)
            raise InjectableImportError(this_object, error=str(e))
        
        for module_name in [
            f"{project_name}.lib.inject.{type.lower()}", f"swayam.inject.{type.lower()}.builtin"]: 
            try:
                injectable_module = importlib.import_module(module_name)
                return getattr(injectable_module, name)
            except ModuleNotFoundError as e:
                # Check with this error is for the current injectable type
                if e.name.endswith(f".lib.inject.{type.lower()}"):
                    pass
                else:
                    import traceback
                    # Extract the stack trace as a list of FrameSummary objects
                    frame = traceback.extract_tb(e.__traceback__)[-1]
                    frame_str = f"File: {frame.filename}, Line: {frame.lineno}, Function: {frame.name}, Code: {frame.line}"
                    raise_import_exception(e.msg + f". Check: {frame_str}")
            except InjectableObjectError as e:
                raise_import_exception(e)
            except AttributeError as e:
                if e.name == name:
                    pass
                else:
                    raise_import_exception(e)  
            except Exception as e:
                raise_import_exception(e)       

        raise InjectableNotFoundError(
                                cls.create_metadata_object(type=type, name=name), caller_file=caller_file)
    @classmethod
    def create_metadata_object(cls, *, type, name, module_name=None):
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
        return InjectableClass(type=type, name=name, module_name=module_name)
    
    @classmethod
    def validate_callable_definition(cls, injectable):
        # Check if it is a callable
        if not kallable(injectable.callable):
            raise InjectableNotCallableError(injectable)
        
        # Get the signature of the function
        signature = inspect.signature(injectable.callable)
        
        for param in signature.parameters.values():
            if param.kind != inspect.Parameter.KEYWORD_ONLY:
                raise InjectableInvalidCallableDefinitionError(injectable, error="Found non-keyword arguments in definition.")
            
        # Extract keyword-only arguments
        keyword_only_params = [
            param for param in signature.parameters.values()
            if param.kind == inspect.Parameter.KEYWORD_ONLY
        ]
        
        # Get the names of these parameters
        keyword_only_names = {param.name for param in keyword_only_params}
        
        # Check if all parameters are keyword-only and match the expected names
        if not keyword_only_names == set(injectable.allowed_keywords):
            raise InjectableInvalidCallableDefinitionError(injectable, error=f"Found {keyword_only_names} in definition.")
        
    @classmethod
    def call(cls, injectable, **kwargs):
        from swayam.inject.structure.structure import IOStructureObject
        try:
            output = injectable.callable(caller=injectable, **kwargs)
        except Exception as e:
            raise InjectableCallError(injectable, error=e)
        else:        
            if not isinstance(output, IOStructureObject):
                raise InjectableInvalidOutputError(injectable, output=output)
            elif output.structure.name != injectable.output_structure.name:
                raise InjectableInvalidOutputError(injectable, output=output.name)
            else:
                return output.as_dict()
        
        
        