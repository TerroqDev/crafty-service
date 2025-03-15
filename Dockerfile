FROM python:3.12-slim
WORKDIR /app

RUN pip install poetry==1.8.3
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 8000

ENTRYPOINT ["poetry"]
CMD ["run", "crafty"]
