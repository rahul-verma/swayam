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

class NamespaceError(Exception):
    
    def __init__(self, ns, *, error):
        super().__init__(f"{ns.name} at {ns.path}: {error}")
        
class NamespaceDoesNotExistError(NamespaceError):
    
    def __init__(self, ns):
        super().__init__(ns, error= f"The Namespace directory for {ns.resolution} does not exist.")
        
class NamespaceIsNotADirectoryError(NamespaceError):
    
    def __init__(self, ns):
        super().__init__(ns, error= f"Expected a directory at the path for {ns.resolution} Namespace. Found a file instead.")
        
class DefinitionNameNotAFileError(NamespaceError):
    
    def __init__(self, ns, *, name):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Definition  >>{name}<< should be a file with .yaml extension. Found a directory instead with {name}")
        
class DefinitionNameNotADirectoryError(NamespaceError):
    
    def __init__(self, ns, *, name):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Definition  >>{name}<< should be a directory. Found a file instead with {name}")
        
class NamespaceDirectoryMissingPackageFileError(NamespaceError):

    def __init__(self, ns, * name):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Namespace  >>{name}<< directory  does not contain the mandatory __init__.yaml file.")   
        
class DefinitionFileWithoutExtensionError(NamespaceError):
    
    def __init__(self, ns, *, name):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Definition file {name} should have a yaml extension.")
        
class DefinitionNotFoundError(NamespaceError):
    
    def __init__(self, ns, *, name, error=""):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Definition file >>{name}.yaml<< not found. Expected path: {ns.path}/{name}.yaml. {error}")
        
class DefinitionIsInvalidError(NamespaceError):
    
    def __init__(self, ns, *, name, path, resolution, error):
        super().__init__(ns, error= f"{resolution}: Definition file >>{name}.yaml<< does not follow the rules for a {ns.type} definition. Path: {path}. Error: {error}")
        
class DefinitionFormattingError(NamespaceError):
    
    def __init__(self, ns, *, name, path, resolution, fmt_kwargs, error):
        super().__init__(ns, error= f"{resolution}: Not able to format Definition file >>{name}.yaml<<. Path: {path}. Provided format dictionary has keys {fmt_kwargs.keys()} : Error: {error}")