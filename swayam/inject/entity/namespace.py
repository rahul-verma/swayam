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

import os
from .entity import Entity
from swayam.namespace.namespace import Namespace
from swayam.namespace.error import *
from swayam.core.caller import get_caller_module_file_location

class EntityNamespace(Namespace):
    
    def __init__(self, path, resolution=None, **fmt_kwargs):
        super().__init__(type="Entity", path=path, resolution=resolution, **fmt_kwargs)  

    def handle_current_name_as_package(self, *, name, path, resolution, **kwargs):
        return EntityNamespace(path=path, resolution=resolution)
    
    def handle_current_name_as_definition(self, *, name, path, resolution, purpose, content):
        from swayam import Template
        import yaml
        content = yaml.safe_load(content)
        from tarkash import Tarkash
        if isinstance(content, dict):
            from swayam.inject.template.builtin.internal import Entity as EntityTemplate
            try:
                return Entity(name=name, **EntityTemplate(**content).as_dict())
            except Exception as e:
                import traceback
                raise DefinitionIsInvalidError(self, name=name, path=path, resolution=resolution, error=f"Allowed dictionary keys are [{EntityTemplate.keys}]. Error: {e}. Check: {traceback.format_exc()} ")
        else:
            raise DefinitionIsInvalidError(self, name=name, path=path, resolution=resolution, error=f"Expected dict, got {type(content)}")
        
        
