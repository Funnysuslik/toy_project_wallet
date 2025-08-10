FROM python:3.12.4-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install -y libpq-dev gcc && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

CMD ["bash", "./entrypoint.sh"]