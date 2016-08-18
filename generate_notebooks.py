import os
import sys
import glob
import shutil
import nbformat as nbf
from nbformat.v4 import reads, writes, new_markdown_cell, new_code_cell, new_notebook
from nbconvert.exporters.notebook import NotebookExporter
import codecs

all_tutorials = []
all_examples = []

###################### GENERATE TUTORIAL NOTEBOOKS ###################################
note = '''
### Quickstart
To run the code below:

1. Click on the cell to select it.
2. Press `SHIFT+ENTER` on your keyboard or press the play button
   (<button class='fa fa-play icon-play btn btn-xs btn-default'></button>) in the toolbar above.

Feel free to create new cells using the plus button
(<button class='fa fa-plus icon-plus btn btn-xs btn-default'></button>), or pressing `SHIFT+ENTER` while this cell
is selected.
<div class="alert alert-warning" role="alert" style="margin: 10px">
<p>**WARNING**</p>
<p>Don't rely on this server for anything you want to last - your server will be
*deleted after 1 hour of inactivity*.</p>
</div>

This notebook is running on [mybinder.org](http://mybinder.org) created by the
[Freeman lab](https://www.janelia.org/lab/freeman-lab).
'''
if not os.path.exists('tutorials'):
    os.mkdir('tutorials')
for notebook in glob.glob('_tutorials/*.ipynb'):
    with open(notebook, 'r') as f:
        content = reads(f.read())
    title = content.cells[0]['source'].split('\n')[0].strip('# ')
    all_tutorials.append((title, notebook[1:].replace('\\', '/')))

    # Insert a note about Jupyter notebooks at the top with a download link
    content.cells.insert(1, new_markdown_cell(note))
    (path, filename) = os.path.split(notebook)

    with open('tutorials/' + filename, 'w') as f:
        nbf.write(content, f)

shutil.rmtree('_tutorials')


###################### GENERATE EXAMPLES NOTEBOOKS ###################################

magic = '''%matplotlib notebook\n'''
if not os.path.exists('examples'):
    os.mkdir('examples')
for root, subfolders, files in os.walk('_examples'):
    for file in files:
        if not file.endswith('.py'):
            continue
        example = os.path.join(root, file)
        all_examples.append((root[10:].replace('\\', '/'), file))
        with open(example, 'r') as f:
            code = f.read()

        (base, ext) = os.path.splitext(os.path.split(example)[-1])

        # Create blank notebook
        content = new_notebook()
        content['cells'] = [new_markdown_cell(note),
                            new_code_cell(magic + code)]

        if not os.path.exists(root[1:]):
            os.mkdir(root[1:])

        exporter = NotebookExporter()
        output, _ = exporter.from_notebook_node(content)
        codecs.open(''.join([root[1:], '/', base, '.ipynb']), 'w', encoding='utf-8').write(output)

shutil.rmtree('_examples')

###################### GENERATE INDEX NOTEBOOK ###################################

all_tutorials.sort(key=lambda (title, fname): fname)
tutorials_index = ''
for title, fname in all_tutorials:
    tutorials_index += '* [{title}]({fname})\n'.format(title=title, fname=fname)
examples_index = ''
curroot = ''
for root, fname in all_examples:
    if curroot!=root:
        examples_index += '\n'+'#'*(root.count('/')+3)+' '+root+'\n\n'
        curroot = root
    if root:
        fullfname = 'examples/'+root+'/'+fname[:-3]+'.ipynb'
    else:
        fullfname = 'examples/'+fname[:-3]+'.ipynb'
    examples_index += '* [{name}]({fullfname})\n'.format(name=fname[:-3], fullfname=fullfname)

with open('index_template.ipynb', 'r') as f:
    indexnb = reads(f.read())

for cell in indexnb['cells']:
    if 'INSERT_TUTORIALS_HERE' in cell['source']:
        cell['source'] = tutorials_index
    if 'INSERT_EXAMPLES_HERE' in cell['source']:
        cell['source'] = examples_index

with open('index.ipynb', 'w') as f:
    nbf.write(indexnb, f)
