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
from .error import *
from abc import ABC, abstractmethod

class Namespace(ABC):
    
    def __init__(self, type, path, *, resolution=None, **fmt_kwargs):
        self.__type = type
        self.__name = f"{self.__type} namespace"
        self.__resolution = resolution
        self.__path = path
        if self.__resolution is None:
            self.__resolution = f"{self.__type}"
        if not os.path.exists(path):
            raise NamespaceDoesNotExistError(self)
        elif not os.path.isdir(path):
            raise NamespaceIsNotADirectoryError(self)
        
        self.__path = path
        
        self.__fmt_kwargs = fmt_kwargs
        
    @property
    def name(self):
        return self.__name
    @property
    def path(self):
        return self.__path
    
    @property
    def resolution(self):
        return self.__resolution
    
    @property
    def type(self):
        return self.__type

    def __getattr__(self, name):
        
        if name.startswith("formatter"):
            from functools import partial
            # Return a partial namespace of the same type
            return self.__class__(path=self.path, resolution=self.resolution, fmt_kwargs=self.__fmt_kwargs)
       
        name_path = os.path.join(self.path, name)
        # Check without the yaml extension
        if os.path.exists(name_path):
            if os.path.isdir(name_path):          
                children = {
                    "package_file": None,
                    "attachments_dir": [],
                    "directories": [],
                    "files": []
                    
                }
            
                for name in os.listdir(name_path):
                    child_path = os.path.join(name_path, name)
                    if os.path.isdir(child_path):
                        if name == "__files__":
                            children["attachments_dir"].append(child_path)
                        else:
                            children["directories"].append(name)
                    elif os.path.isfile(child_path):
                        if name  == "__init__.yaml":
                            children["package_file"] = child_path
                        elif name.endswith(".yaml"):
                            children["files"].append(name[:-5])
                            
                if children["package_file"] is None:
                    self.handle_no_package_file()
                else: 
                    with open(children["package_file"]) as f:
                        content = f.read()
                        content.format(**self.__fmt_kwargs)
                        children["package_file_content"] = content
                
                return self.handle_current_name_as_package(
                    name=name,
                    path=name_path,
                    resolution=self.resolution + "." + name,
                    package_file_content=children["package_file_content"],
                    sub_directories = children["directories"],
                    definitions = children["files"],
                )
            else:
                raise DefinitionFileWithoutExtensionError(self, name)
        elif os.path.exists(name_path + ".yaml"):
            content = None
            with open(name_path + ".yaml") as f:
                content = f.read()
            return self.handle_current_name_as_definition(
                    name=name,
                    path=name_path + ".yaml",
                    resolution=self.resolution + "." + name,
                    purpose = name.replace("_", " ").title(),
                    content=content.format(**self.__fmt_kwargs)
                )
        else:
            raise DefinitionNotFoundError(self, name=name)
        
    def handle_no_package_file(self):
        pass
    
    @abstractmethod
    def handle_current_name_as_package(self, *, name, path, resolution, package_file_content, sub_directories, definitions):
        pass
    
    @abstractmethod
    def handle_current_name_as_definition(self, *, name, path, resolution, purpose, content):
        pass