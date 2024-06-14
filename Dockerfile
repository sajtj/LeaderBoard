FROM python:3.9

WORKDIR /app

ADD poetry.lock pyproject.toml /app/
RUN pip3 install poetry
RUN poetry install
# RUN mkdir /app

ADD ./ /app/

CMD [ "poetry run python -m web.manage runserver 0.0.0.0:8000" ]`