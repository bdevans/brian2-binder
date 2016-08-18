FROM andrewosh/binder-base

MAINTAINER Ben Evans <ben.d.evans@gmail.com>

USER main

RUN conda config --add channels brian-team
RUN conda install --quiet --yes \
    'pip=8.1*' \
    #sphinx \
    #coverage \
    'matplotlib=1.5*' \
    'cython=0.24*' \
    'nose=1.3*' \
    'brian2' \
    'brian2tools'

RUN conda install --quiet --yes -n python3 \
    'pip=8.1*' \
    #sphinx \
    #coverage \
    'matplotlib=1.5*' \
    'cython=0.24*' \
    'nose=1.3*' \
    'brian2' \
    'brian2tools'

### Generate tutorials/examples notebooks and move to working directory
WORKDIR $HOME

RUN git clone git://github.com/brian-team/brian2.git
RUN mv brian2/tutorials _tutorials
RUN mv brian2/examples _examples
RUN rm -rf brian2

# Modify tutorials and genenate new notebooks from examples
COPY generate_notebooks.py .
RUN python generate_notebooks.py
RUN rm generate_notebooks.py

RUN chmod -R +x tutorials
RUN chmod -R +x examples

#RUN mkdir notebooks
RUN mv tutorials notebooks/tutorials
RUN mv examples notebooks/examples
RUN mv index.ipynb notebooks/index.ipynb

# Give ownership to 'main' user to allow saving of notebooks
USER root
RUN chown -R main:main $HOME/notebooks/tutorials
RUN chown -R main:main $HOME/notebooks/examples
USER main

RUN find ./notebooks -name '*.ipynb' -exec jupyter trust {} \;

# Fix matplotlib font cache
RUN rm -rf /home/main/.matplolib
RUN rm -rf /home/main/.cache/matplolib
RUN rm -rf /home/main/.cache/fontconfig
RUN python -c "import matplotlib.pyplot as plt"
