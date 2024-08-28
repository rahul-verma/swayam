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

from swayam.inject.error import *

_NAME = "Snippet"

class SnippetNotFoundError(InjectedNameNotFoundError):
    
    def __init__(self, name):
        super().__init__(_NAME, name)
        
class SnippetImportError(InjectedNameImportError):
    
    def __init__(self, name, *, import_error_message):
        super().__init__(_NAME, name, import_error_message=import_error_message)
        
class SnippetArgIsNotCallableError(InjectedObjectCallableArgError):
    
    def __init__(self, name, callable):
        super().__init__(_NAME, name, kallable=callable)
        
class SnippetDefinitionFormatError(InjectableObjectError):
    
    def __init__(self, name, *, path, error):
        super().__init__(_NAME, name, f"Unexpected format of YAML in definition at {path}. Error: {error}")
        
class SnippetDefinitionNotFoundError(InjectableObjectError):
    
    def __init__(self, name, *, path):
        super().__init__(_NAME, name, "There is neither a directory nor a YAML file with the name {name} at path {path}.")
        
class SnippetCallableOutputError(InjectableObjectCallableOutputError):
    
    def __init__(self, name, *, actual_object):
        super().__init__(_NAME, name, actual_object=actual_object, expected_type="Structure.Snippet")