
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# #                                                                Incomplete like a nincompoop from here on
# def get_hotels(city: str) -> list:
#     api_key = os.getenv("SERPAPI_API_KEY")
#     url = f'https://serpapi.com/search'
    
#     params = {
#         'api_key':api_key,
#         'engine':'google_hotels',
#         'q':city,
#         'currency':'INR',
#         'check_in_date':,
#         'check_out_date':,
#     }

#     try:
#         response = requests.get(url, params=params)
#         data = response.json()
#         hotels = []
#         print(data)


#     except Exception as e:
#         print(f"[Hotels Service] Error: {e}")
#         return []
    

# hotels = get_hotels("Goa")

# print(hotels)


"""
test_serper_hotels.py — run this to see EXACTLY what Serper returns for a
hotel-style query, so we can write the real parser instead of guessing.

    pip install requests
    python test_serper_hotels.py
"""

import os
import json
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def search_hotels(
    city: str,
    budget: int, 
    limit: int = 5,
    check_in: Optional[str] = None,
    check_out: Optional[str] = None
) -> list[dict]:
    API_KEY = os.getenv("SERPER_API_KEY", "")

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": API_KEY, 
        "Content-Type": "application/json"
    }

    params={
        "q": f"hotels in {city} under {budget}", 
        "gl": "us", 
        "hl": "en"
    }

    resp = requests.post(
        url,
        headers=headers,
        json=params,
        timeout=15,
    )

    print("STATUS:", resp.status_code)
    print("TOP-LEVEL KEYS:", list(resp.json().keys()))
    print()
    print("FULL BODY:")
    print(json.dumps(resp.json(), indent=2)[:8000])  # first 4000 chars, plenty to see the shape
