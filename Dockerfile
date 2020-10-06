FROM quay.io/keboola/docker-custom-python:latest

ADD requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . /code/
WORKDIR /data/
CMD ["python", "-u", "/code/src/main.py"]
