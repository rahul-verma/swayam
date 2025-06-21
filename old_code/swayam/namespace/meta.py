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

class NamespaceMeta(type):
    def __new__(cls, name, bases, class_dict):
        class_dict['root'] = "NOT_SET"
        return super(NamespaceMeta, cls).__new__(cls, name, bases, class_dict)
    
    def load_root_namespace(cls, option_name, namespace_class):
        if cls.root == "NOT_SET":
            from tarkash import Tarkash
            cls.root = namespace_class(Tarkash.get_option_value(option_name))