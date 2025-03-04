FROM alpine:latest
RUN apk update
RUN apk add --no-cache python3 py3-pip python3-dev
WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 5000
CMD ["venv/bin/flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000", "--debug", "--reload"]
