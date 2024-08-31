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


class ExpressionMeta(type):
    
    def __getattr__(cls, name):
        from .file import ExpressionFileLoader
        if name == "file":
            return ExpressionFileLoader()
        elif name == "repeater":
            from .repeater import ExpressionFileRepeater
            return ExpressionFileRepeater
        
        from .namespace import ExpressionDir
        return ExpressionDir.load_expression_from_file(name)