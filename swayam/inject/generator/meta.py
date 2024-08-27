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

import importlib

from .error import *

class GeneratorMeta(type):
    
    def __getattr__(cls, name):
        from swayam.inject.structure.error import StructureNotFoundError
        from swayam.inject.tool.error import ToolNotFoundError
        try:
            from tarkash import Tarkash, TarkashOption
            project_name = Tarkash.get_option_value(TarkashOption.PROJECT_NAME)
            generator_module = importlib.import_module(f"{project_name}.lib.inject.generator")
            return getattr(generator_module, name)
        except (StructureNotFoundError, ToolNotFoundError, NameError, ) as e:
            raise GeneratorImportError(name, import_error_message=str(e))
        except (ModuleNotFoundError, AttributeError) as e:
            pass
        
        try:
            generator_module = importlib.import_module("swayam.inject.generator.builtin")
            return getattr(generator_module, name)
        except (StructureNotFoundError, ToolNotFoundError, NameError) as e:
            raise GeneratorImportError(name, import_error_message=str(e))
        except AttributeError as e:
            pass
        
        
        raise GeneratorNotFoundError(name)