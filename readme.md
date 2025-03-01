
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
```


## Docker

``` bash
sudo make app-up
sudo make app-down
sudo make app
sudo make ps


sudo docker compose up -d

```



etc

[Туториал](https://github.com/dpills/fastapi-prod-guide)