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

import yaml

from swayam.namespace.namespace import Namespace
from swayam.namespace.error import *
from swayam.core.caller import get_caller_module_file_location

class ExpressionNamespace(Namespace):
    
    def __init__(self, path, resolution=None, **fmt_kwargs):
        super().__init__(type="Expression", path=path, resolution=resolution, **fmt_kwargs)  
    
    def handle_current_name_as_definition(self, *, name, path, resolution, purpose, content):
        raise DefinitionNameNotADirectoryError(self, name=name)
    
    def handle_no_package_file(self):
        raise NamespaceDirectoryMissingPackageFileError(self)

    def handle_current_name_as_package(self, *, name, path, resolution, package_file_content, sub_directories, definitions):
        from .expression import UserExpression
        from swayam import Template
            
        import yaml
        expression_dict = yaml.safe_load(package_file_content)
        if isinstance(expression_dict, dict):
            from swayam.inject.template.builtin.internal import Expression
            try:
                expression = UserExpression(name=name, **Expression(**expression_dict).as_dict())
            except Exception as e:
                import traceback
                raise DefinitionIsInvalidError(self, name=name, path=path, resolution=resolution, error=f"Allowed dictionary keys are [{Expression.keys}]. Overall template definition is {str(Expression.definition)}. Error: {e}. Check: {traceback.format_exc()} ")
            
            expression.load(prompt_ns_path=path, resolution=resolution, **self.fmt_kwargs)
            return expression
        else:
            raise DefinitionIsInvalidError(self, name=name, path=path, resolution=resolution, error=f"Expected dict, got {type(expression_dict)}")
        
        
        
        
        
        