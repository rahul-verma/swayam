import os, sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
        
base_path = os.environ["TEMP_IMPORT_PATH"]
for path in ["tarkash", "swayam"]:
    sys.path.append(os.path.join(base_path, path)) 

from tarkash import Tarkash
Tarkash.init()

from swayam import Swayam
Swayam.init()


