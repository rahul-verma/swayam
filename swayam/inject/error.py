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
    
    def __init__(self, injectable, *, error):
        self.__type = injectable.type
        self.__name = injectable.name
        super().__init__(f"{injectable.type} >>{injectable.name}<<: {error}")
        
    @property
    def injectable_type(self):
        return self.__type
    
    @property
    def injectable_name(self):
        return self.__name

class InjectableNotFoundError(InjectableObjectError):
    
    def __init__(self, injectable, caller_file=None):
        if caller_file is not None:
            suffix = f"Further Info: The >>{injectable.type}.{injectable.name}<< call originated from the file {caller_file}."
        else:
            suffix = ""
        super().__init__(injectable, error=f"Neither defined in the project, nor defined by Swayam. {suffix}")
        
class  InjectableImportError(InjectableObjectError):
    
    def __init__(self, injectable, *, error):
        name = f"Module: {injectable.module_name}.{injectable.name}"
        super().__init__(injectable, error=f"Object was found, but could not be imported. Check definition for {injectable.type} >>{name}<< for spelling/casing errors. The error might originate in another place in your injection lib, rather than the {injectable.type.lower()} {injectable.name}. Check your project injection lib. Error: {error}")
        
class InjectableNotCallableError(InjectableObjectError):
    
    def __init__(self, injectable):
        super().__init__(injectable, error=f"Got object >>{injectable.callable} of type >>{injectable.callable.__name__}<<. Expected a callable object.")
        
class InjectableInvalidInputStructureError(InjectableObjectError):
    
    def __init__(self, injectable, *, provided_input, error=""):
        super().__init__(injectable, error=f"The provided input is >>{str(provided_input)}<<. Expected: >>Template.{injectable.in_template.name}<<.{error}")
        
class InjectableInvalidInputContentError(InjectableObjectError):
        
        def __init__(self, injectable, *, provided_input, error):
            super().__init__(injectable, error=f"The provided input is structurally correct, but failed content validation. Provided Input: {provided_input}. Error: {error}")
        
class InjectableInvalidCallableDefinitionError(InjectableObjectError):
    
    def __init__(self, injectable, *, error):
        super().__init__(injectable, error=f"Unexpected {injectable.callable} definition. Expected a callable definition with these keyword-only arguments: {injectable.allowed_keywords!r}. Error: {error}")
        
class InjectableCallError(InjectableObjectError):

    def __init__(self, injectable, *, error):
            super().__init__(injectable, error=f"A run-time error happened when {injectable.callable.__name__} was called. Error: {error}")
        
class InjectableOutputNotAStructureError(InjectableObjectError):
    
    def __init__(self, injectable, *, output):
        super().__init__(injectable, error=f"Expected callable >>{injectable.callable}<< to return object of type >>Template.{injectable.out_template.name}<<. Got >>{str(output)}<< of type >>{type(output)} instead: {str(output)}.")
    
class InjectableInvalidOutputStructureError(InjectableObjectError):
    
    def __init__(self, injectable, *, output):
        super().__init__(injectable, error=f"Expected callable >>{injectable.callable}<< to return object of type >>Template.{injectable.out_template.name}<<. Got an output template of type >>{output.name}<< instead with data: {str(output.as_dict())}.")
        
class InjectableDefinitionNotFoundError(InjectableObjectError):
    
    def __init__(self, injectable, definition):
        super().__init__(injectable, error="There is neither a directory nor a YAML file with the name {definition.name} at path {definition.path}.")
        
class InjectableDefinitionFormatError(InjectableObjectError):
    
    def __init__(self, injectable, *, error):
        super().__init__(injectable, error=f"Unexpected format of YAML in definition at {injectable.path}. Error: {error}")
        
