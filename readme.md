
# Тестовое приложение

API with stack: 
* fastapi
* mongo
* poetry
* docker
* kubernetes


## Poetry 

```bash
poetry init
poetry add fastapi 'uvicorn[standard]'
poetry add -G dev ruff black mypy
poetry add python-dotenv pydantic-settings motor
poetry add -G dev pytest coverage mongomock-motor pytest_httpx pytest-asyncio
```


## Docker

``` bash
sudo make app-up
sudo make app-down
sudo make app
sudo make ps

sudo docker compose up -d

```

## Mongo

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

```


```
https://github.com/login/oauth/authorize?client_id=Ov23lizZ77UiHHRUDa4i&redirect_uri=http://localhost:8000/v1/auth/callback
```


access_token": "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"

etc

[Tutorial](https://dev.to/dpills/fastapi-production-setup-guide-1hhh)
[Git](https://github.com/dpills/fastapi-prod-guide)