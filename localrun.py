import os, shutil, brian2

b2dir, _ = os.path.split(brian2.__file__)

for dname in ['examples', '_examples',
              'tutorials', '_tutorials']:
    if os.path.exists(dname):
        shutil.rmtree(dname)

shutil.copytree(os.path.abspath(os.path.join(b2dir, '../examples')), '_examples')
shutil.copytree(os.path.abspath(os.path.join(b2dir, '../tutorials')), '_tutorials')
os.mkdir('examples')
os.mkdir('tutorials')

exec(open('generate_notebooks.py', 'r').read())
