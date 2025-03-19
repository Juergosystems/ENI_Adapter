FROM python:3.10.6-slim
WORKDIR /eni_adapter
COPY requirements.txt /eni_adapter/
RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . /eni_adapter/
EXPOSE 5000
ENTRYPOINT ["bash", "/eni_adapter/bin/run.sh"]
