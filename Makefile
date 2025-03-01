D = docker
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose.yml
APP_CONTAINER = main-app



.PHONY: ps
ps:
	${D} ps


.PHONY: logs
logs:
	${D} logs ${APP_CONTAINER} 


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-up
app-up:
	${DC} -f ${APP_FILE} ${ENV} up --build



.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f
