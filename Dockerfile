FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04
COPY requirements.txt /opt/
COPY package.json /opt/
COPY sources.list /etc/apt/

ENV PATH="${PATH}:/opt/node-v12.14.0-linux-x64/bin"

RUN rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get install -y \
        ffmpeg \
        curl \
        python3.6 \
        python3-pip \
        xz-utils \
        libsm6 libxext6 libxrender-dev \
        --no-install-recommends \
    && curl -O https://nodejs.org/dist/v12.14.0/node-v12.14.0-linux-x64.tar.xz \
    && tar -xf node-v12.14.0-linux-x64.tar.xz --no-same-owner -C /opt/ \
    && cd /opt/ && npm install --registry=https://registry.npm.taobao.org \
    && python3.6 -m pip install -i https://repo.huaweicloud.com/repository/pypi/simple -r /opt/requirements.txt