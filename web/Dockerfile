FROM hub.hamdocker.ir/python:3.10


WORKDIR /app

ADD poetry.lock pyproject.toml /app/
RUN pip3 install poetry
RUN poetry install
# RUN mkdir /app

ADD ./ /app/
