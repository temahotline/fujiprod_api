# FUJIPROD API

Fujiprod API - это веб-приложение, разработанное с использованием FastAPI, которое предоставляет RESTful API для управления данными музыкального издательства, приложение хранит данные пользователей и данные о их релизах  


## Запуск приложения

1. Поднимаем Docker-Compose 

```
make up
```

2. Накатываем миграции
```
docker-compose -f docker-compose-local.yaml exec app alembic upgrade head
```
3. Открывваем документацию в браузере
```
http://0.0.0.0:8000/docs
```
или
```
http://0.0.0.0:8000/redoc
```

