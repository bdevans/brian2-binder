FROM andrewosh/binder-base

MAINTAINER Ben Evans <ben.d.evans@gmail.com>

USER main

RUN conda config --add channels brian-team
RUN conda install --quiet --yes \
    pip \
    sphinx \
    coverage \
    'matplotlib=1.5*' \
    'cython=0.23*' \
    'nose=1.3*' \
    'brian2' \
    'brian2tools'

RUN conda install --quiet --yes -n python3 \
    pip \
    sphinx \
    coverage \
    'matplotlib=1.5*' \
    'cython=0.23*' \
    'nose=1.3*' \
    'brian2' \
    'brian2tools'

#RUN pip install brian2tools
#RUN /home/main/anaconda2/envs/python3/bin/pip install brian2tools
