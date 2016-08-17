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
RUN git clone git://github.com/brian-team/brian2.git
RUN mv brian2/tutorials .
RUN mv brian2/examples .
RUN rm -rf brian2
RUN chmod -R +x tutorials
RUN chmod -R +x examples

RUN chown -R $NB_USER:users /home/$NB_USER/work


# Fix matplotlib font cache
RUN rm -rf /home/main/.matplolib
RUN rm -rf /home/main/.cache/matplolib
RUN rm -rf /home/main/.cache/fontconfig
RUN python -c "import matplotlib.pyplot as plt"
