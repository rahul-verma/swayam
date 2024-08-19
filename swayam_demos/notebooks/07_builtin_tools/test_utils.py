import os, sys
base_path = "/Users/rahulverma/Documents/GitHub"
for path in ["tarkash", "swayam"]:
    sys.path.append(os.path.join(base_path, path)) 

from swayam import Swayam
Swayam.init()


