# FROM python:3.10 as requirements

# # WORKDIR /app
# # ADD . .
# RUN pip3 install poetry
# ADD poetry.lock pyproject.toml ./
# RUN pip wheel --no-cache-dir --use-pep517 "psycopg2==2.9.1"
# RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt

# FROM python:3.10 as webapp
# COPY --from=requirements /scr/requirements.txt .
# RUN pip install -r requirements.txt

# # RUN poetry config virtualenvs.create false --local
# # RUN poetry install
# # ADD ./ /app/

# # CMD ["poetry", "run", "python", "-m", "web.manage", "runserver", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.10

WORKDIR /app

ADD poetry.lock pyproject.toml /app/
RUN pip3 install poetry
ADD ./ /app/
RUN poetry config virtualenvs.create false --local
RUN poetry install


CMD ["poetry", "run", "python", "-m", "web.manage", "runserver", "0.0.0.0:8000"]