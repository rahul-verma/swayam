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

from swayam.namespace.meta import NamespaceMeta
from swayam.core.caller import get_caller_module_file_location
from swayam import Entity
from .reference import Reference
    
class ReferenceMeta(NamespaceMeta):
    
    def __getattr__(cls, name):
        ref_file_name = f"{name}.json"
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        folio_draft_dir = Tarkash.get_option_value(SwayamOption.FOLIO_BLUEPRINT_DIR)
        reference_file_path = os.path.join(folio_draft_dir, ref_file_name)
        if not os.path.exists(reference_file_path):
            # Look for generated name
            reference_file_path = os.path.join(folio_draft_dir, "generated_" + ref_file_name)
            if not os.path.exists(reference_file_path):
                from .error import ReferenceContentNotFoundError
                raise ReferenceContentNotFoundError(name=name)
        return Reference(name, file_path=reference_file_path)