FROM python:3.10

WORKDIR /app

ADD poetry.lock pyproject.toml /app/
RUN pip3 install poetry
ADD ./ /app/
RUN poetry config virtualenvs.create false --local
RUN poetry install


CMD ["poetry", "run", "python", "-m", "web.manage", "runserver", "0.0.0.0:8000"]