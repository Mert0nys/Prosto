import asyncio
import aiohttp

class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public"
    
    async def fetch_price(self, index_name):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/get_index_price?index_name={index_name}") as response:
                data = await response.json()
                print(f"🔍 {index_name}: {data}")
                return data
    
    async def get_prices(self):
        btc_data = await self.fetch_price('btc_usdc')
        eth_data = await self.fetch_price('eth_usdc')
        
        btc_price = float(btc_data['result']['index_price']) if btc_data.get('result') else None
        eth_price = float(eth_data['result']['index_price']) if eth_data.get('result') else None
        
        return btc_price, eth_price