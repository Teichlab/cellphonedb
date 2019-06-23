ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION

RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt
COPY . /app

CMD python -m unittest