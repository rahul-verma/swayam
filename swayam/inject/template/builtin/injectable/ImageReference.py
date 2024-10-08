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

from typing import Union
from pydantic import BaseModel, Field
from .Reference import ReferenceContentModel
from .FileInfo import FileInfoModel
from swayam import Template

class ImageReferenceModel(ReferenceContentModel):
    reference_image_name: str = Field(None, description="Path to the image file associated with the reference. Same as file_path if present.")
    reference_image_file_path: str = Field(description="Path to the image file associated with the reference. Same as file_path if present.")

ImageReference = Template.build("ImageReference", model=ImageReferenceModel)