FROM mambaorg/micromamba:bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV MAMBA_NO_BANNER=true
ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV NVIDIA_VISIBLE_DEVICES=all

USER root

RUN apt-get update && apt-get install -y build-essential wget git

USER mambauser
RUN micromamba create -n textgen -c main python=3.10.9
RUN micromamba run -n textgen pip install torch --index-url https://download.pytorch.org/whl/cu121

RUN echo "micromamba activate textgen" >> ~/.bashrc

WORKDIR /opt/text-generation-webui
RUN git clone https://github.com/oobabooga/text-generation-webui .
RUN git checkout 7b9ad64

RUN micromamba run -n textgen pip install -r requirements.txt
RUN micromamba run -n textgen pip uninstall -y auto-gptq
RUN micromamba run -n textgen pip install auto-gptq
RUN micromamba install -n textgen -c "nvidia/label/cuda-12.0.0" cuda-toolkit -y

RUN micromamba run -n textgen pip uninstall llama-cpp-python -y
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 micromamba run -n textgen pip install -v llama-cpp-python --no-cache-dir
RUN cp /opt/conda/envs/textgen/lib/python3.10/site-packages/bitsandbytes/libbitsandbytes_cuda120.so /opt/conda/envs/textgen/lib/python3.10/site-packages/bitsandbytes/libbitsandbytes_cpu.so

COPY --chmod=777 download-and-run.sh .

ENTRYPOINT ["micromamba", "run", "-n", "textgen", "./download-and-run.sh"]
