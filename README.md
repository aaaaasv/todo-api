# TODO API

## General info

Backend API with the functionalities of a TODO app.

## Built with

* [Python 3.8](https://www.python.org/)
* [FastAPI 0.65.2](https://fastapi.tiangolo.com/)

## Setup

1. Clone the repository:

```sh
$ git clone https://github.com/aaaaasv/todo-api.git
$ cd todo-api
```

2. Run:

```sh
$ docker-compose up --build
```

And navigate to `http://127.0.0.1:8000`.

## Usage

On the `/docs` or `/redoc` pages, you can find API documentation.

### Authentication

Application supports JSON Web Tokens:

* `users/token` - to obtain a new token

### Tests

```
$ docker-compose exec web pytest
```