FROM nikolaik/python-nodejs:python3.11-nodejs18

# 1. Update pip
RUN pip install --upgrade pip setuptools wheel

# 2. Add cmake to the list of build tools
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        tzdata \
        gcc \
        g++ \
        python3-dev \
        git \
        cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/

# 3. Install dependencies from the Git links
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]
