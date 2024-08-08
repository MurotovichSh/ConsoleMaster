FROM python:3

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    python3-opengl \
    libsdl2-dev \
    libsdl2-ttf-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    x11-apps && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

