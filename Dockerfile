FROM nikolaik/python-nodejs:python3.11-nodejs18

# 1. Update pip and essential build tools
RUN pip install --upgrade pip setuptools wheel

# 2. Install ffmpeg AND tzdata (helps with time sync errors)
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Setup application directory
WORKDIR /app
COPY . /app/

# 4. Install dependencies
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# 5. Start the bot (ensure main.py is in the root folder)
CMD ["python", "main.py"]
