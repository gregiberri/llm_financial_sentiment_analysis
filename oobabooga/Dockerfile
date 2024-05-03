FROM mambaorg/micromamba:bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV MAMBA_NO_BANNER=true
ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV NVIDIA_VISIBLE_DEVICES=all

USER root

RUN apt-get update && apt-get install -y build-essential wget git

USER mambauser
RUN micromamba create -n textgen -c main python=3.10.9
RUN micromamba install -n textgen -c nvidia cuda-toolkit=11.7 cudatoolkit=11.7 -y

RUN micromamba run -n textgen pip install torch --index-url https://download.pytorch.org/whl/cu117

RUN echo "micromamba activate textgen" >> ~/.bashrc

WORKDIR /opt/text-generation-webui
RUN git clone https://github.com/oobabooga/text-generation-webui .
RUN git checkout 7b9ad64

RUN micromamba run -n textgen pip install -r requirements.txt
RUN micromamba run -n textgen pip install https://github.com/jllllll/AutoGPTQ/releases/download/v0.6.0/auto_gptq-0.6.0+cu117-cp310-cp310-linux_x86_64.whl

RUN micromamba run -n textgen pip uninstall llama-cpp-python -y
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 micromamba run -n textgen pip install -v llama-cpp-python --no-cache-dir
RUN cp /opt/conda/envs/textgen/lib/python3.10/site-packages/bitsandbytes/libbitsandbytes_cuda117.so /opt/conda/envs/textgen/lib/python3.10/site-packages/bitsandbytes/libbitsandbytes_cpu.so

RUN micromamba run -n textgen pip cache purge && micromamba clean --all -y

COPY --chmod=777 download-and-run.sh .

ENTRYPOINT ["micromamba", "run", "-n", "textgen", "./download-and-run.sh"]
