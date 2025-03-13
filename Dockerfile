# Используем официальный образ Ubuntu как базовый
FROM ubuntu:22.04

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    tar \
    libncurses5-dev \
    libncursesw5-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем Python-скрипт в контейнер
COPY build_t2_iso.py /app/

# Устанавливаем права на выполнение (если нужно)
RUN chmod +x /app/build_t2_iso.py

# Задаем команду по умолчанию
CMD ["python3", "build_t2_iso.py"]