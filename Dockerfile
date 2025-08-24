FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install fastapi uvicorn mysql-connector-python python-multipart

WORKDIR /app

COPY main.py .

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000","--reload"]
