from IPython.display import display, HTML, Markdown
from redlines import Redlines

from .html import convert_to_html

def display_as_html(text):
    display(convert_to_html(text))
    
def display_diff(source, revision):
    diff = Redlines(source,revision)
    display(Markdown(diff.output_markdown))