import aiohttp
from config import API_KEY, BASE_URL  # BASE_URL = "https://5sim.net/v1/"

class FiveSimAPI:
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def _log(self, action, url, params=None, response=None, error=None):
        print(f"\n[DEBUG] {action}")
        print(f"URL: {url}")
        if params:
            print(f"Params: {params}")
        if response:
            print(f"Response: {response}")
        if error:
            print(f"Error: {error}")

    async def fetch(self, endpoint, params=None):
        url = self.base_url + endpoint
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.headers.get("Content-Type", "").startswith("application/json"):
                        return await response.json()
                    else:
                        text = await response.text()
                        return {"error": f"Unexpected response format:\n{text}"}
        except Exception as e:
            return {"error": str(e)}

    async def post(self, endpoint, data=None):
        url = self.base_url + endpoint
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=data) as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    # ------------------ 🧾 User ------------------
    async def get_profile(self):
        return await self.fetch("user/profile")

    async def get_balance(self):
        return await self.fetch("user/profile")

    async def get_order_history(self, category="activation", limit=15, offset=0, order="id", reverse=True):
        params = {
            "category": category,
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": str(reverse).lower()
        }
        return await self.fetch("user/orders", params)

    async def get_payment_history(self, limit=15, offset=0, order="id", reverse=True):
        params = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": str(reverse).lower()
        }
        return await self.fetch("user/payments", params)

    # ------------------ 🌐 Guest ------------------
    async def get_services(self, country="any"):
        return await self.fetch(f"guest/products/{country}")

    async def get_prices(self, product=None, country=None):
        if product and country:
            return await self.fetch(f"guest/prices?product={product}&country={country}")
        return await self.fetch("guest/prices")

    async def get_countries(self):
        return await self.fetch("guest/countries")

    async def get_operators(self, country='any'):
        return await self.fetch(f"guest/operators/{country}")

    # ------------------ 📲 Activation Orders ------------------
    async def buy_activation(self, product, country, operator=None):
        params = {"product": product, "country": country}
        if operator:
            params["operator"] = operator
        return await self.fetch("user/buy/activation", params)

    async def get_sms(self, order_id):
        return await self.fetch(f"user/check/{order_id}")

    async def cancel_order(self, order_id):
        return await self.post(f"user/cancel/{order_id}")

    async def finish_order(self, order_id):
        return await self.post(f"user/finish/{order_id}")

    async def ban_order(self, order_id):
        return await self.post(f"user/ban/{order_id}")

    # ------------------ 🏷️ Rent Orders ------------------
    async def rent_number(self, product, country, operator=None, hours=1, quantity=1):
        params = {
            "product": product,
            "country": country,
            "hours": hours,
            "quantity": quantity
        }
        if operator:
            params["operator"] = operator
        return await self.fetch("user/buy/rent", params)

    async def get_rent_status(self, rent_id):
        return await self.fetch(f"user/rent/{rent_id}")

    async def cancel_rent(self, rent_id):
        return await self.post(f"user/rent/{rent_id}/cancel")

    async def finish_rent(self, rent_id):
        return await self.post(f"user/rent/{rent_id}/finish")

    # ------------------ 💳 Top-Up ------------------
    async def get_topup_methods(self):
        return await self.fetch("user/top-up/methods")

    async def get_topup_links(self, amount, currency="usd"):
        return await self.fetch(f"user/top-up?amount={amount}&currency={currency}")

    # ------------------ 🧪 Test ------------------
    async def test_connection(self):
        profile = await self.get_profile()
        return "username" in profile

