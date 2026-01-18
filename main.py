from sqlalchemy.future import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Price
from database import get_db
from client import DeribitClient
import datetime

app = FastAPI()

@app.get('/prices')
async def get_prices(ticker: str, fetch_latest: bool = False, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Price).filter(Price.ticker == ticker))
    prices = result.scalars().all()
    if fetch_latest or not prices:
        client = DeribitClient()
        index_name = ticker.replace('_usd', '_usdc') if 'usd' in ticker else ticker      
        data = await client.fetch_price(index_name)
        if data.get('result'):
            price_value = float(data['result']['index_price'])
            timestamp = datetime.datetime.now()  
            new_price = Price(ticker=ticker, price=int(price_value), timestamp=timestamp)
            db.add(new_price)
            await db.commit()
            await db.refresh(new_price)
            prices.append(new_price)
    return prices

@app.get('/prices/latest')
async def get_latest_price( ticker: str, fetch_latest: bool = False, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Price).filter(Price.ticker == ticker).order_by(Price.timestamp.desc()).limit(1)
    )
    price = result.scalar_one_or_none()
    if not price or fetch_latest:
        client = DeribitClient()
        index_name = ticker.replace('_usd', '_usdc') if 'usd' in ticker else ticker        
        data = await client.fetch_price(index_name)
        if data.get('result'):
            price_value = float(data['result']['index_price'])
            timestamp = datetime.datetime.now()
            price = Price(ticker=ticker, price=int(price_value), timestamp=timestamp)
            db.add(price)
            await db.commit()
            await db.refresh(price)   
    return price

@app.get('/prices/filter')
async def get_price_by_date(ticker: str, date: str, db: AsyncSession = Depends(get_db)):
    dt = datetime.datetime.fromisoformat(date.replace('Z', '+00:00'))
    result = await db.execute(
        select(Price).filter(Price.ticker == ticker, Price.timestamp >= dt.replace(tzinfo=None), Price.timestamp < (dt + datetime.timedelta(days=1)).replace(tzinfo=None)
        )
    )
    return result.scalars().all()
