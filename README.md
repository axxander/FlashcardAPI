# FastAPI Flashcard Application

CRUD RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) for managing
flashcards.

## Motivation
The main motivation for this project was to apply new-found knowledge on HTTP and build a 
RESTful API with FastAPI. Additionally, I also learnt about:
- RESTful framework + implementing endpoints using array of HTTP verbs.
- Appropriate status codes for endpoints + consideration behind best practise.
- Relational databases with SQLite3 + CRUD.
- Object-relational mapping (ORM), specifically tortoise-ORM library (asynchronous implementation
  of Django ORM).
- Asynchronous programming: FastAPI and tortoise-ORM both support this.
- JSON Web Tokens, OAuth2.0 and dependency injection.
- Structuring large applications--seperation of concerns.
- Generally improved my programming skills. Shifted from scientific programming
  paradigm formulae->program to more program->product.

## Roadmap
There are many components of the application that need improving. These include:
- Protecting the admin endpoints--I left them as a placeholder for future development.
  Perhaps utilise FastAPI-admin or build another implementation as a learning exercise.
- Unit tests for all components:
  - Database + queries
  - Endpoint responses (what is expected for valid and invalid requests?)
  - Business logic
- Build a frontend for the application by responding with dynamically generated HTML using
  Jinja2 template engine.
- Migrate from SQLite3 to PostgreSQL to simulate production ready application.
- Containerisation--Docker?

## Installation

Install dependencies with [pip](https://pip.pypa.io/en/stable/)...
```bash
pip install -r requirements.txt
```

Assuming source code exists in directory `app`, spin up server with 
[uvicorn](https://www.uvicorn.org/)...

```bash
uvicorn app.main:app --reload
```

Generate secret key for JWT signature, stored in `app/.env` file...

```bash
echo SECRET_KEY=$(openssl rand -hex 32) >> .env
```

## Web Routes + Documentation

All routes are available on `/docs` or `/redoc` paths with Swagger or ReDoc.

## Tests
Coming soon! Currently learning how to do testing for database + API application.