# Базовый образ (Ubuntu с Python)
FROM ubuntu:22.04

ENV HTTP_PROXY="http://130.100.7.222:1082"
ENV HTTPS_PROXY="http://130.100.7.222:1082"

RUN echo 'Acquire::http::Proxy "http://130.100.7.222:1082";' > /etc/apt/apt.conf.d/00aptproxy

# Обновляем систему и устанавливаем Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN apt clean && apt update && apt install curl -y
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

# Рабочая директория
WORKDIR /workspace

# Копируем зависимости
COPY pyproject.toml Makefile /workspace
RUN poetry config virtualenvs.create false
RUN pip install --upgrade pip
RUN make install
ENV PYTHONPATH=/workspace