from celery import Celery
from client import DeribitClient
from database import AsyncSessionLocal
from models import Price
import datetime, asyncio

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def get_and_save_prices():
    asyncio.run(_async_save_prices())

async def _async_save_prices():
    client = DeribitClient()
    btc_price, eth_price = await client.get_prices()
    
    async with AsyncSessionLocal() as db:
        timestamp = datetime.datetime.now()
        
        if btc_price:
            btc = Price(ticker='btc_usdc', price=int(float(btc_price)), timestamp=timestamp)
            db.add(btc)
        
        if eth_price:
            eth = Price(ticker='eth_usdc', price=int(float(eth_price)), timestamp=timestamp)
            db.add(eth)
        
        await db.commit()
