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
    
    def __init__(self, type, path, def_extension="yaml", *, resolution=None, **fmt_kwargs):
        self.__type = type
        self.__name = f"{self.__type} namespace"
        self.__def_extension = def_extension
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
    
    @property
    def fmt_kwargs(self):
        return self.__fmt_kwargs

    def __getattr__(self, def_name):
        
        if def_name == "formatter":
            from functools import partial
            # Return a partial namespace of the same type
            return partial(self.__class__, path=self.path, def_extension=self.__def_extension, resolution=self.resolution)
        
        if "." in def_name:
            prefix, def_name = def_name.split(".", 1)
            return getattr(self.__class__(path=os.path.join(self.path, prefix), def_extension=self.__def_extension, resolution=self.resolution + "." + prefix), def_name)
        
        name_path = os.path.join(self.path, def_name)
        
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
                        if name  == f"__init__.{self.__def_extension}":
                            children["package_file"] = child_path
                        elif name.endswith(self.__def_extension):
                            children["files"].append(name[:-5])
                            
                if children["package_file"] is None:
                    self.handle_no_package_file()
                    children["package_file_content"] = None
                else: 
                    with open(children["package_file"]) as f:
                        content = f.read()
                        children["package_file_content"] = content
                        
                    for k,v in self.fmt_kwargs.items():
                        children["package_file_content"] = children["package_file_content"].replace("$" + k + "$", str(v))
                
                return self.handle_current_name_as_package(
                    name=def_name,
                    path=name_path,
                    resolution=self.resolution + "." + name,
                    package_file_content=children["package_file_content"],
                    sub_directories = children["directories"],
                    definitions = children["files"],
                )
            else:
                raise DefinitionFileWithoutExtensionError(self, name)
        elif os.path.exists(name_path + f".{self.__def_extension}"):
            content = None
            with open(name_path + f".{self.__def_extension}") as f:
                content = f.read()
            try:
                for k,v in self.fmt_kwargs.items():
                    content = content.replace("$" + k + "$", str(v))
                return self.handle_current_name_as_definition(
                        name=def_name,
                        path=name_path + f".{self.__def_extension}",
                        resolution=self.resolution + "." + def_name,
                        purpose = def_name.replace("_", " ").title(),
                        content=content
                )
            except IndexError as e:
                import traceback
                raise DefinitionFormattingError(self, name=def_name, path=name_path + f".{self.__def_extension}", resolution=self.resolution, fmt_kwargs=self.fmt_kwargs, error=f"Are you using a positional placeholders in your {self.__def_extension.upper()} file? Only named placeholders are allowed. " + traceback.format_exc())
            except KeyError as e:
                import traceback
                raise DefinitionFormattingError(self, name=def_name, path=name_path + f".{self.__def_extension.upper()}", resolution=self.resolution, fmt_kwargs=self.fmt_kwargs, error=traceback.format_exc())
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