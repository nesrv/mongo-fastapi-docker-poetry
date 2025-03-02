# Тестовое приложение

API with stack:

- fastapi
- mongo
- poetry
- docker
- kubernetes

## Local Run

```bash
python3 -m app.main
# uvicorn.run( "app.main:app", host="0.0.0.0", port=8000, log_level="debug",reload=True,)
uvicorn main:app --reload
uvicorn main:app --host 85.159.231.14 --port 80 --workers 4
uvicorn main:app --host 0.0.0.0 --port 80000 --workers 4

```

## Deploy

```bash
poetry add gunicorn

TMPDIR=/tmp gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app

gunicorn -k uvicorn.workers.UvicornWorker --worker-tmp-dir /tmp -c gunicorn_conf.py app.main:app

gunicorn -k uvicorn.workers.UvicornWorker --preload -c gunicorn_conf.py app.main:app

sudo mkdir -p /tmp/shm
sudo chmod 1777 /tmp/shm
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app
```

## Poetry

```bash
poetry init
poetry add fastapi 'uvicorn[standard]'
poetry add -G dev ruff black mypy
poetry add python-dotenv pydantic-settings motor
```

## Docker

```bash
sudo make app-up
sudo make app-down
sudo make app
sudo make ps
sudo docker compose up -d

```

# Mongo

```bash
mongosh mongodb://root:mySecureDbPassword1@localhost:27017/
use todoDb
db.tokens.createIndex( { "access_token_hash": 1 }, { unique: true } )

db.tokens.createIndex( { "created_date": 1 }, { expireAfterSeconds: 86400 } )

db.todos.createIndex( { "user": 1 })
db.todos.createIndex( { "_id": 1, "user": 1 })
```

## Auth

```shell
curl -v http://localhost:8000/v1/todos
curl -v http://localhost:8000/v1/todos -H 'Authorization: Bearer gho_...'

```

[github.com/login/oauth/authorize](https://github.com/login/oauth/authorize?client_id=Ov23lizZ77UiHHRUDa4i&redirect_uri=http://localhost:8000/v1/auth/callback)

## Tests

```bash
poetry add -G dev pytest coverage mongomock-motor pytest_httpx pytest-asyncio
export TESTING=true && poetry run coverage run --source ./app -m pytest --disable-warnings
poetry run coverage html
```

etc

[Tutorial](https://dev.to/dpills/fastapi-production-setup-guide-1hhh)

[Git](https://github.com/dpills/fastapi-prod-guide)
