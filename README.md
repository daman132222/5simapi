# 📦 FiveSim API Wrapper for Python (Async)

A fully asynchronous Python wrapper for the [5sim.net API](https://5sim.net/docs), created and maintained by **@damansaini**. This wrapper provides easy access to all key endpoints of 5sim including buying numbers, checking balance, viewing order/payment history, and more.

---

## ✅ Features

- 📱 Buy virtual numbers
- 💵 Check balance
- 📜 Order and payment history
- 🌍 List services, operators, and prices by country
- ❌ Cancel orders
- 🛠️ Well-documented and easy to use
- 🔒 Secure and supports Bearer token

---

## 📦 Installation

```bash
pip install aiohttp
```

---

## 🔧 Configuration (`config.py`)

```python
API_KEY = "your_5sim_api_key"
BASE_URL = "https://5sim.net/v1/"
```

---

## 🚀 Usage Example

```python
from fivesim import FiveSimAPI
import asyncio

api = FiveSimAPI()

async def main():
    profile = await api.get_balance()
    print(profile)

    operators = await api.get_operators("us")
    print(operators)

    history = await api.get_order_history()
    print(history)

asyncio.run(main())
```

---

## 📘 Documentation

### 🔐 User Profile
```python
await api.get_balance()
```
Returns your balance and profile info.

### ❌ Cancel Order
```python
await api.cancel_order(order_id)
```
Cancels a previously placed order.

### 🌐 Operators
```python
await api.get_operators(country='any')
```
Returns list of available operators in a given country.

### 🛍️ Services (Products)
```python
await api.get_services(country='any')
```
Returns list of available services for a country.

### 🧾 Order History
```python
await api.get_order_history(category="activation", limit=15)
```
Returns list of past orders.

### 💳 Payment History
```python
await api.get_payment_history(limit=15)
```
Returns list of past payments.

---

## 🧪 Full Source

```python
import aiohttp
from config import API_KEY, BASE_URL

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

    async def get_balance(self):
        return await self.fetch("user/profile")

    async def cancel_order(self, order_id):
        try:
            url = f"{self.base_url}cancel/{order_id}"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers) as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_operators(self, country='any'):
        return await self.fetch(f"guest/operators/{country}")

    async def get_services(self, country='any'):
        return await self.fetch(f"guest/products/{country}")

    async def get_order_history(self, category="activation", limit=15, offset=0, order="id", reverse=True):
        params = {
            "category": category,
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": str(reverse).lower()
        }
        return await self.fetch("user/orders", params=params)

    async def get_payment_history(self, limit=15, offset=0, order="id", reverse=True):
        params = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": str(reverse).lower()
        }
        return await self.fetch("user/payments", params=params)
```

---

## 🤝 Credits

- Developed by [@damansaini](https://github.com/daman132222)
- Inspired by [5sim.net API Docs](https://5sim.net/docs)

---

## 🧾 License

This project is licensed under the MIT License.
