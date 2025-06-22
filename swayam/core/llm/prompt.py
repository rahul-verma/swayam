import os
from swayam.core.util.file import TextFile

class PromptFile:
    
    def __init__(self, dotname, **kwargs):
        self.__name = dotname
        self.__file = TextFile(os.path.join(os.environ["PROJECT_PATH"], "plib", *self.__name.split(".")) + ".md")
        
        # This should be improved for better data handling
        def get_text(inobj):
            try:
                return inobj.text
            except:
                return str(inobj)

        if kwargs:
            processed_kwargs = {k:get_text(v) for k,v in kwargs.items()}
            self.__text = self.__file.text.format(**processed_kwargs)
        else:
            self.__text = self.__file.text
        
       
    @property
    def text(self):
        return self.__text
    
class PromptText:
    
    def __init__(self, text, **kwargs):
        self.__text = text
        if kwargs:
            self.__text = self.__text.format(**{k:v.text for k,v in kwargs.items()})
       
    @property
    def text(self):
        return self.__text

        
    