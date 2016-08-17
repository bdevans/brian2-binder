import os  # , sys, shutil, glob, codecs
import glob
import fnmatch
import nbformat as nbf
from nbformat.v4 import reads, writes, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.exporters.notebook import NotebookExporter
from nbconvert.exporters.rst import RSTExporter

#notebooks = [f for f in os.listdir('_tutorials') if f.endswith('.ipynb')]
#examples = [f for f in os.listdir('_examples') if f.endswith('.py')]

note = u'''
### Quickstart
To run the code below:

1. Click on the cell to select it.
2. Press `SHIFT+ENTER` on your keyboard or press the play button (<button class='fa fa-play icon-play btn btn-xs btn-default'></button>) in the toolbar above.

Feel free to create new cells using the plus button (<button class='fa fa-plus icon-plus btn btn-xs btn-default'></button>), or pressing `SHIFT+ENTER` while this cell is selected.
<div class="alert alert-warning" role="alert" style="margin: 10px">
<p>**WARNING**</p>
<p>Don't rely on this server for anything you want to last - your server will be *deleted after 10 minutes of inactivity*.</p>
</div>
'''

#os.chdir("_tutorials")
for notebook in glob.glob('_tutorials/*.ipynb'):
    with open(notebook, 'r') as f:
        content = reads(f.read())

    # Insert a note about Jupyter notebooks at the top with a download link
    content.cells.insert(1, new_markdown_cell(note))
    (path, filename) = os.path.split(notebook) #[-1]

    with open('tutorials/' + filename, 'w') as f:
        nbf.write(content, f)


magic = u'''%matplotlib notebook\n'''

for example in glob.iglob('_examples/**/*.py', recursive=True):
#for root, subFolders, files in os.walk('_examples'):
    #for example in fnmatch.filter(files, '*.py'):
        #os.path.join(root, example)
    #for example in glob.glob('_examples/*.py'):
    #for example in files:
    with open(example, 'r') as f:
        code = f.read()

    (base, ext) = os.path.splitext(os.path.split(example)[-1])

    # Create blank notebook
    content = nbf.v4.new_notebook()
    content['cells'] = [new_markdown_cell(note),
                        new_code_cell(magic + code)]

    #notebook = ''.join(['examples/', base, '.ipynb'])
    with open(''.join(['examples/', base, '.ipynb']), 'w') as f:
        nbf.write(content, f)
