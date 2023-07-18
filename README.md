# SMIT_task
## Описание

Данный сервис разработан для расчета стоимости страхования в зависимости от типа груза и объявленной стоимости

<details>
<summary>ТЗ проекта ↓</summary>

Реализовать REST API сервис по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости (ОС).
Тариф должен загружаться из файла JSON или должен принимать подобную JSON структуру:

```json
{
  "2020-06-01": [
    {
      "cargo_type": "Glass",
      "rate": 0.25
    },
    {
      "cargo_type": "Other",
      "rate": 0.01
    }
  ],
  "2020-07-01": [
    {
      "cargo_type": "Glass",
      "rate": 0.035
    },
    {
      "cargo_type": "Other",
      "rate": 0.01567
    }
  ]
} 
```
* Сервис должен посчитать стоимость страхования для запроса используя актуальный тариф.(Загружается через API)
* Сервис возвращает (объявленную стоимость * rate) в зависимости от указанного в запросе типа груза и даты.
* Сервис должен разворачиваться внутри Docker.
* Сервис должен разрабатываться через GIT (Файл Readme с подробным описанием развертывания)
* Данные должны храниться в базе данных
* Технологии, которые должны быть использованы при реализации тестового задания:
FastApi,
Tortoise ORM,
Postgresql, Mysql, Sqlite (любой на выбор),
Docker.
</details>

## Используемые технологии

![AppVeyor](https://img.shields.io/badge/Python-3.10.6-green)
![AppVeyor](https://img.shields.io/badge/FastAPI-0.100.0-9cf)
![AppVeyor](https://img.shields.io/badge/Aerich-0.7.1-9cf)
![AppVeyor](https://img.shields.io/badge/TortoiseORM-0.19.3-9cf)
![AppVeyor](https://img.shields.io/badge/pytest-7.4.0-9cf)
![AppVeyor](https://img.shields.io/badge/pydantic-2.0.3-9cf)
![AppVeyor](https://img.shields.io/badge/uvicorn-0.23.0-9cf)

![AppVeyor](https://img.shields.io/badge/Docker-24.0.2-green)
![AppVeyor](https://img.shields.io/badge/docker--compose-1.29.2-9cf)

![AppVeyor](https://img.shields.io/badge/Postgres-15.0-green)

![AppVeyor](https://img.shields.io/badge/Poetry-1.5.1-green)

## Запуск

###  Локально

1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/SMIT_task.git
   ```
2. Переходим в директорию с проектом:
    ```bash
    cd app/
    ```
3. Создаем .env файл и заполняем в соответствии с примером (.env.example).

4. Устанавливаем зависимости:
    ```bash
    poetry install
    ```
5. Накатываем миграции:
   ```bash
   aerich upgrade
   ```
6. Загружаем данные из файла data.json (при необходимости заполняем своими данными):
   ```bash
   python upload_data/script.py
   ```
7. Запускаем приложение:
   ```bash
   python main.py
   ```
###  Докер
1. Клонируем репозиторий:
   ```bash
    git clone https://github.com/Timoha23/SMIT_task.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Поднимаем контейнеры:
   ```bash
   docker-compose up -d --build
   ```
## Примеры запросов
1. Просмотр всех дат с тарифами
    * Endpoint: **host:port/**
    * Method: **GET**
    * Response:
      ```json
      [
        {
          "2020-06-01": [
            {
              "cargo_type": "Glass",
              "rate": 0.25
            },
            {
              "cargo_type": "Other",
              "rate": 0.01
            }
          ]
        },
        {
          "2020-07-01": [
            {
              "cargo_type": "Glass",
              "rate": 0.035
            },
            {
              "cargo_type": "Other",
              "rate": 0.0157
            }
          ]
        }
      ]
      ```
2. Получение стоимости страхового тарифа:
    * Endpoint: **host:port/get_price/**
    * Method: **POST**
    * Body:
      ```json
      {
        "date": "string",
        "cargo_type": "string",
        "declared_price": 0
      }
      ```
    * Response:
      ```json
      {
        "date": "string",
        "insurance_price": 0,
        "declared_price": 0,
        "cargo": {
          "type": "string",
          "rate": 0
        }
      }
      ```