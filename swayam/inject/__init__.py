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
    def raise_import_exception(cls, type, name, module_name, e):
        this_object = Injectable.create_metadata_object(type=type, name=name, module_name=module_name)
        raise InjectableImportError(this_object, error=str(e))

    @classmethod
    def extract_caller_from_frame(cls, frame):
        return f"File: {frame.filename}, Line: {frame.lineno}, Function: {frame.name}, Code: {frame.line}"
    
    @classmethod
    def load_module(cls, type, name, caller_file=None):
    
        type = type.lower()
        from tarkash import Tarkash, TarkashOption
        project_name = Tarkash.get_option_value(TarkashOption.PROJECT_NAME)

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
                    frame = traceback.extract_tb(e.__traceback__)[-1]
                    cls.raise_import_exception(type, name, module_name, str(e) + f". Check: {cls.extract_caller_from_frame(frame)}")
            except InjectableObjectError as e:
                import traceback
                frame = traceback.extract_tb(e.__traceback__)[-1]
                cls.raise_import_exception(type, name, module_name, str(e) + f". Check: {cls.extract_caller_from_frame(frame)}")
            except AttributeError as e:
                if e.name == name:
                    pass
                else:
                    import traceback
                    frame = traceback.extract_tb(e.__traceback__)[-1]
                    cls.raise_import_exception(type, name, module_name, str(e) + f". Check: {cls.extract_caller_from_frame(frame)}") 
            except Exception as e:
                import traceback
                frame = traceback.extract_tb(e.__traceback__)[-1]
                cls.raise_import_exception(type, name, module_name, str(e) + f". Check: {cls.extract_caller_from_frame(frame)}")       

        raise InjectableNotFoundError(
                                cls.create_metadata_object(type=type, name=name), caller_file=caller_file)
    @classmethod
    def create_metadata_object(cls, *, type, name, module_name=None):
        class InjectableClass:
            def __init__(self, type, name, module_name):
                print(type)
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
        
        
        