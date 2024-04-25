FROM ubuntu:22.04 

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash
ENV MAMBA_NO_BANNER=true
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

WORKDIR /code

RUN apt update
RUN apt install -y software-properties-common build-essential openssh-server git screen tmux htop curl

# making micromamba dir and adding permissions to user
RUN mkdir /opt/micromamba && chmod -R 777 /opt/micromamba

# install micromamba
ENV MAMBA_ROOT_PREFIX="/root/miniforge3"
ENV PATH "$MAMBA_ROOT_PREFIX/bin:$PATH"
ENV PYTHONPATH "/code:$PYTHONPATH"
ENV PYTHONHASHSEED=0
RUN curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" && bash Miniforge3-$(uname)-$(uname -m).sh -b

# create env
COPY environment.yml /environment.yml
RUN mamba env create -f /environment.yml

# install git lfs
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt install -y git-lfs && git lfs install

ENTRYPOINT ["mamba", "run", "--no-capture-output", "-n", "llm_sentiment"]
CMD ["jupyter", "lab", "--allow-root", "--debug", "--ip=0.0.0.0", "--NotebookApp.token=''", "--NotebookApp.password=''", "--notebook-dir=/code"]
