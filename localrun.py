import os, shutil

for dname in ['examples', '_examples',
              'tutorials', '_tutorials']:
    if os.path.exists(dname):
        shutil.rmtree(dname)

shutil.copytree('brian2/examples', '_examples')
shutil.copytree('brian2/tutorials', '_tutorials')
os.mkdir('examples')
os.mkdir('tutorials')

#execfile('generate_notebooks.py')
