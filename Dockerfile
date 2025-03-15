from python:3.13-slim as builder
run apt-get update && apt-get upgrade -y \
    && apt-get install -y libmariadb-dev gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
workdir /app
copy requirements.txt .
run pip wheel --no-cache-dir --no-deps \
    --wheel-dir /app/wheels -r requirements.txt

from python:3.13-slim
run apt-get update && apt-get upgrade -y \
    && apt-get install -y libmariadb-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
run addgroup --system audiovault && adduser --system --group audiovault
env HOME /home/audiovault
workdir $HOME
run mkdir ./movies && mkdir ./shows
copy requirements.txt .
copy --from=builder /app/wheels /wheels
run pip install --upgrade pip && pip install --no-cache /wheels/*
copy app app
copy migrations migrations
copy boot.sh config.py main.py .
env PATH_FOR_MOVIES $HOME/movies/
env PATH_FOR_SHOWS $HOME/shows/
expose 5000
run chown -R audiovault:audiovault .
user audiovault
run chmod 755 boot.sh
cmd ["./boot.sh"]