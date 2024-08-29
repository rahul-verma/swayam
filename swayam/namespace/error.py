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
        
class DefinitionFileWithoutExtensionError(NamespaceError):
    
    def __init__(self, ns, *, name):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Definition file {name} should have a yaml extension.")
        
class DefinitionNotFoundError(NamespaceError):
    
    def __init__(self, ns, *, name):
        super().__init__(ns, error= f"{ns.resolution}.{name}: Definition file >>{name}.yaml<< not found. Expected path: {ns.path}/{name}.yaml")
        
class DefinitionIsInvalidError(NamespaceError):
    
    def __init__(self, ns, *, name, path, resolution, error):
        super().__init__(ns, error= f"{resolution}: Definition file >>{name}.yaml<< does not follow the rules for a {ns.type} definition. Path: {path}. Error: {error}")