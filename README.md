# Crafty FastAPI Project

This project is a FastAPI application set up with Poetry for dependency management. It includes a development server using Uvicorn with automatic reloading enabled.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Contributing](#contributing)

## Requirements

- Python 3.12.4
- Poetry

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/marijamatijevi/crafty.git
cd crafty
```

### Step 2: Set Up the Virtual Environment

Using Poetry:

```bash
poetry install
```

## Configuration

### Step 1: Set Up Environment Variables

Create a .env file in the root of the project with the following content:

APP_ENV=development
DATABASE_URL=mysql+pymysql://root:1234@localhost:3306/crafty

Adjust DATABASE_URL with your actual database credentials and hostname.

### Step 2: Update the Database URL

Ensure the DATABASE_URL in your .env file is correct. It should follow this format:

mysql+pymysql://username:password@hostname:port/database


## Database Migrations

Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine.

[Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) is mainly being used as
a migration tool. We can create manual migrations by using the following command:

```bash
alembic revision -m "create account table"
```

Migrations can also be automatically created using `--autogenerate`:

```bash
alembic revision --autogenerate -m "Added account table"
```

More on that can be found here https://alembic.sqlalchemy.org/en/latest/autogenerate.html

To run the migrations we can specify a revision we’d like to upgrade to, but it’s easier in most cases just to tell it “the most recent”, in this case head:

```bash
alembic upgrade head
```

Migrations can also be downgraded. Revision can be specified or the number of migrations we would like to downgrade. So if we specify `-2` we will downgrade 2 migrations.

```bash
alembic downgrade -1
```

All commands mentioned here are only examples. More information about how to use Alembic migrations can be found at the tutorial page.

**IMPORTANT:** When using a new database first run the server so all tables get created. After that you will need to specify the newest migration version by using `alembic stamp head` or by using the revision `alembic stamp 27c6a30d7c24`. This is used to prevent migrations from crashing when using a clean database. Once the database is created again it will contain all tables as they are defined in the db models. However, Alembic won't know that these changes are already in the database since table `alembic_version`, which tracks the newest migration version, is missing.


## Running the Application

### Start the Development Server

Run the application with Uvicorn:

```bash
poetry run uvicorn crafty.main:app --reload
```

or just run:

```bash
crafty
```

This will start the development server. You can access the application at http://localhost:4000.
