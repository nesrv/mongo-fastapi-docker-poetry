# Тестовое приложение

API with stack:

- fastapi
- mongo
- poetry
- docker
- kubernetes

## Local Run

```bash
+ python3 -m app.main
+ gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
# uvicorn.run( "app.main:app", host="0.0.0.0", port=8000, log_level="debug",reload=True,)
uvicorn main:app --reload
uvicorn main:app --host 85.159.231.14 --port 80 --workers 4
uvicorn main:app --host 0.0.0.0 --port 80000 --workers 4



```

## Deploy


```bash
poetry add gunicorn

- TMPDIR=/tmp gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app

+ gunicorn -k uvicorn.workers.UvicornWorker --worker-tmp-dir /tmp -c gunicorn_conf.py app.main:app

- gunicorn -k uvicorn.workers.UvicornWorker --preload -c gunicorn_conf.py app.main:app

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
poetry shell
uvicorn main:app --reload
```

## Docker

```bash
sudo make app-up
sudo make app-down
sudo make app (sudo docker compose up -d)
sudo make ps

docker build . -t fastapi-todos:1.0.0

+ sudo docker build -t fastapi-todos .
sudo docker run -p 8000:80 fastapi-todos

+ sudo docker run -p 8000:80 --env-file .env fastapi-todos


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


[Запуск FastAPI на gunicorn + uvicorn workers](https://rutube.ru/video/ee219d5807899134ba794f170bb5dafc/?playlist=392620)

[гит к видео](https://github.com/mahenzon/fastapi-users-intro)

[Tutorial](https://dev.to/dpills/fastapi-production-setup-guide-1hhh)

[Git](https://github.com/dpills/fastapi-prod-guide)
