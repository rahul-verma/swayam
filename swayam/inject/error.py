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

class InjectableObjectError(Exception):
    
    def __init__(self, injectable, error):
        super().__init__(f"{injectable.type} >>{injectable.name}<<: {error}")

class InjectableNameNotFoundError(InjectableObjectError):
    
    def __init__(self, injectable):
        super().__init__(injectable, "Neither defined in the project, nor defined by Swayam.")
        
class  InjectableNameImportError(InjectableObjectError):
    
    def __init__(self, injectable, *, error):
        name = f"Module: {injectable.module_name}.{injectable.name}"
        super().__init__(injectable, f"Object was found, but could not be imported. Error: {error}. Check definition for {injectable.type} >>{name}<< for spelling/casing errors, else check your project hook lib.")
        
class InjectableNotCallableError(InjectableObjectError):
    
    def __init__(self, injectable):
        super().__init__(injectable, f"Got object >>{injectable.callable} of type >>{type(injectable.callable)}<<. Expected a callable object.")
        
class InjectableInvalidInputError(InjectableObjectError):
    
    def __init__(self, injectable, *, provided_input):
        super().__init__(injectable, message=f"The provided input is >>{provided_input}<<. Expected: {injectable.input_structure.definition!r}.")
        
class InjectableInvalidCallableDefinitionError(InjectableObjectError):
    
    def __init__(self, injectable):
        super().__init__(injectable, message=f"Unexpected {injectable.callable} definition. Expected a callable definition with these keyword-only arguments: {injectable.keywords!r}.")
        
class InjectableCallError(InjectableObjectError):

    def __init__(self, injectable, *, error):
            super().__init__(injectable, message=f"A run-time error happened when {injectable.callable} was called. Error: {error}")
        
class InjectableInvalidOutputError(InjectableObjectError):
    
    def __init__(self, injectable, *, output):
        super().__init__(injectable, f"Expected callable >>{injectable.callable}<< to return object of type >>{injectable.output_structure}<<. Got >>{output}<< of type >>{type(output)} instead.")
        
class InjectableDefinitionNotFoundError(InjectableObjectError):
    
    def __init__(self, injectable, definition):
        super().__init__(injectable, "There is neither a directory nor a YAML file with the name {definition.name} at path {definition.path}.")
        
class InjectableDefinitionFormatError(InjectableObjectError):
    
    def __init__(self, injectable, *, error):
        super().__init__(injectable, f"Unexpected format of YAML in definition at {injectable.path}. Error: {error}")
        
