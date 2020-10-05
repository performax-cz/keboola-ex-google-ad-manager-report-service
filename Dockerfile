FROM quay.io/keboola/docker-custom-python:latest

ARG PYPI_USER
ARG PYPI_PASSWORD
RUN mkdir -p ~/.pip && echo "[global]\nextra-index-url = https://$PYPI_USER:$PYPI_PASSWORD@pip.performax.cz/simple" > ~/.pip/pip.conf

ADD requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . /code/
WORKDIR /data/
CMD ["python", "-u", "/code/src/main.py"]
