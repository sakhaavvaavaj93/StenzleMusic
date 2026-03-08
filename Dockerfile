FROM nikolaik/python-nodejs:python3.11-nodejs18

# 1. Update pip
RUN pip install --upgrade pip setuptools wheel

# 2. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        libavcodec-dev \
        libavformat-dev \
        libavutil-dev \
        libswresample-dev \
        libswscale-dev \
        tzdata \
        gcc \
        g++ \
        python3-dev \
        git \
        cmake \
        pkg-config \
        libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app
COPY . /app/

# 3. Install dependencies from the Git links
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]
