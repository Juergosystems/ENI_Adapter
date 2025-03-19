FROM python:3.10.6-slim
WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . /app/
WORKDIR /app
EXPOSE 5000
ENTRYPOINT ["bash", "/app/bin/run.sh"]
