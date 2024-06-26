# Use the official Python base image
FROM python:3.9

RUN apt-get upgrade
RUN apt-get update && apt-get install -y \
    build-essential \
    procps \
    curl \
    git \
    zlib1g-dev \
    locales \
    unrar-free \
    ffmpeg

WORKDIR /app

RUN pip install jupyter
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]