FROM andrewosh/binder-base

MAINTAINER Ben Evans <ben.d.evans@gmail.com>

USER main

RUN conda config --add channels brian-team
RUN conda install --quiet --yes \
    'pip=8.1*' \
    #sphinx \
    #coverage \
    'matplotlib=1.5*' \
    'cython=0.23*' \
    'nose=1.3*' \
    'brian2' \
    'brian2tools'

RUN conda install --quiet --yes -n python3 \
    'pip=8.1*' \
    #sphinx \
    #coverage \
    'matplotlib=1.5*' \
    'cython=0.23*' \
    'nose=1.3*' \
    'brian2' \
    'brian2tools'

### Copy demonstration notebook and config files to home directory
WORKDIR $HOME
#USER root

RUN git clone git://github.com/brian-team/brian2.git
RUN mv brian2/tutorials _tutorials
RUN mv brian2/examples _examples
RUN rm -rf brian2

#RUN chown -R $USER:users $HOME/_tutorials
#RUN chown -R $USER:users $HOME/_examples

# Modify tutorials and genenate new notebooks from examples
COPY generate_notebooks.py .
RUN python generate_notebooks.py
RUN rm generate_notebooks.py

RUN chmod -R +x tutorials
RUN chmod -R +x examples

RUN mkdir notebooks
RUN mv tutorials notebooks/tutorials
RUN mv examples notebooks/examples

RUN find ./notebooks -name '*.ipynb' -exec jupyter trust {} \;
#USER $USER

# Fix matplotlib font cache
RUN rm -rf /home/main/.matplolib
RUN rm -rf /home/main/.cache/matplolib
RUN rm -rf /home/main/.cache/fontconfig
RUN python -c "import matplotlib.pyplot as plt"
