FROM nikolaik/python-nodejs:python3.11-nodejs18
RUN pip install --upgrade pip
RUN pip install --upgrade "lxml>=6.0.0"
RUN pip install --upgrade pip setuptools wheel
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

CMD bash Stenzle
