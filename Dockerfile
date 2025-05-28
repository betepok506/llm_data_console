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

# Рабочая директория
WORKDIR /workspace

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt