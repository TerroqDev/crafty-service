FROM python:3.12-slim

# Install dependencies for wait-for-it and curl
RUN apt-get update && apt-get install -y curl

# Download the wait-for-it script
RUN curl -sSLo /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry==1.8.3

# Copy necessary project files
COPY pyproject.toml poetry.lock alembic.ini ./

# Copy the rest of the application
COPY . .

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry lock --no-update && poetry install --no-dev

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=.
