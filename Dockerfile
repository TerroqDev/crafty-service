FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock alembic.ini ./
COPY . .

RUN poetry config virtualenvs.create false && poetry lock --no-update && poetry install --no-dev

ENV PYTHONPATH=.

ENTRYPOINT ["poetry"]
CMD ["run", "crafty"]