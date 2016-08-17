import os
import sys
import glob
import nbformat as nbf
from nbformat.v4 import reads, writes, new_markdown_cell, new_code_cell
from nbconvert.exporters.notebook import NotebookExporter
import codecs

note = '''
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

for notebook in glob.glob('_tutorials/*.ipynb'):
    with open(notebook, 'r') as f:
        content = reads(f.read())

    # Insert a note about Jupyter notebooks at the top with a download link
    content.cells.insert(1, new_markdown_cell(note))
    (path, filename) = os.path.split(notebook) #[-1]

    with open('tutorials/' + filename, 'w') as f:
        nbf.write(content, f)


magic = '''%matplotlib notebook\n'''

for root, subfolders, files in os.walk('_examples'):
    for file in files:
        if not file.endswith('.py'):
            continue
        example = os.path.join(root, file)
        with open(example, 'r') as f:
            code = f.read()

        (base, ext) = os.path.splitext(os.path.split(example)[-1])

        # Create blank notebook
        content = nbf.v4.new_notebook()
        content['cells'] = [new_markdown_cell(note),
                            new_code_cell(magic + code)]

        if not os.path.exists(root[1:]):
            os.mkdir(root[1:])

        exporter = NotebookExporter()
        output, _ = exporter.from_notebook_node(content)
        codecs.open(''.join([root[1:], '/', base, '.ipynb']), 'w', encoding='utf-8').write(output)
