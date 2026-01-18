# Crypto Price Tracker

## Описание
Данное приложение отслеживает цены на BTC и ETH с биржи Deribit и сохраняет их в базу данных PostgreSQL.

## Установка 
1. Установите зависимости:
   <code>pip install -r requirements.txt</code>
   
2. Настройте базу данных PostgreSQL и создайте таблицу.

3. Запустите Celery worker:
   <code>celery -A tasks worker --loglevel=info</code>
   
4. Запустите FastAPI:
   <code>uvicorn main:app --reload</code>
