FROM python:3.11-slim  as requirements-stage

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false


WORKDIR /tmp

RUN pip install --upgrade pip && \
    pip install "poetry==${POETRY_VERSION}"


COPY ./pyproject.toml ./poetry.lock* /tmp/


RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim 

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
 
COPY ./pyproject.toml ./gunicorn_conf.py /
# COPY ./app /app



RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN echo 'bind = "0.0.0.0:8000"\n\
workers = 4\n\
worker_class = "uvicorn.workers.UvicornWorker"\n\
loglevel = "info"\n\
accesslog = "-"\n\
errorlog = "-"' > /code/gunicorn_conf.py

COPY ./app /code/app

COPY ./.env /code/.env

# RUN mkdir -p /tmp/shm && mkdir /.local

# ENV PORT 8000
# EXPOSE 8000

# ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "app.main:app"]
CMD ["sh", "-c", "env && gunicorn -k uvicorn.workers.UvicornWorker -c /gunicorn_conf.py app.main:app"]
