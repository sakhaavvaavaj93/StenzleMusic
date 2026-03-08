FROM nikolaik/python-nodejs:python3.11-nodejs18

# 1. Update pip and essential build tools
RUN pip install --upgrade pip setuptools wheel

# 2. Install ffmpeg, tzdata, AND build essentials (added cmake)
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

# 3. Setup application directory
WORKDIR /app
COPY . /app/

# 4. Install dependencies
# This will now successfully compile ntgcalls v2.1.0+
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# 5. Start the bot
CMD ["python", "main.py"]
