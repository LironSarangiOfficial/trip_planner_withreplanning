import requests

import os

from dotenv import load_dotenv

load_dotenv()

def get_hotels(city: str) -> list:
    api_key = os.getenv("FOURSQUARE_API_KEY")
    url = "https://api.foursquare.com/v3places/search"
    headers = {"Authorization": api_key}
    params = {
        "query":"hotel",
        "near": f"{city},India",
        "limit": 5
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        hotels = []
        for result in data.get("results", []):
            hotels.append({
                "name": result["name"],
                "address": result["location"].get("formatted_address", "")
            })

        return hotels

    except Exception as e:
        print(f"[Hotels Service] Error: {e}")
        return []
 

# import os
# import requests
# from dotenv import load_dotenv


# load_dotenv()

# FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
# FOURSQUARE_API_VERSION = os.getenv("FOURSQUARE_API_VERSION", "2025-06-17")

# if FOURSQUARE_API_KEY:
#     FOURSQUARE_API_KEY = FOURSQUARE_API_KEY.strip().strip('"').strip("'")

# if FOURSQUARE_API_VERSION:
#     FOURSQUARE_API_VERSION = FOURSQUARE_API_VERSION.strip().strip('"').strip("'")


# def foursquare_enabled() -> bool:
#     """
#     Returns True if Foursquare API key is available.
#     """
#     return bool(FOURSQUARE_API_KEY)


# def search_hotels_foursquare(place: str, limit: int = 5) -> dict:
#     """
#     Searches hotels near a destination using Foursquare new Places API.

#     Important:
#     - No hardcoded hotel names.
#     - No hardcoded hotel prices.
#     - Uses price/rating/distance only if Foursquare provides them.
#     """

#     if not FOURSQUARE_API_KEY:
#         return {
#             "error": "FOURSQUARE_API_KEY missing",
#             "hotels": []
#         }

#     if not place:
#         return {
#             "error": "Destination place is missing",
#             "hotels": []
#         }

#     url = "https://places-api.foursquare.com/places/search"

#     headers = {
#     "Authorization": FOURSQUARE_API_KEY,
#     "Accept": "application/json",
#     "X-Places-Api-Version": FOURSQUARE_API_VERSION
#     }

#     params = {
#         "query": "hotel",
#         "near": f"{place}, India",
#         "limit": limit
#     }

#     try:
#         print("===== FOURSQUARE HOTEL SEARCH CALLED =====")
#         print("Hotel search place:", place)
#         print("Request URL:", url)
#         print("Foursquare API version:", FOURSQUARE_API_VERSION)
#         print(
#             "Foursquare key loaded:",
#             FOURSQUARE_API_KEY[:6] + "..." + FOURSQUARE_API_KEY[-4:]
#         )

#         response = requests.get(
#             url,
#             headers=headers,
#             params=params,
#             timeout=30
#         )

#         print("Final URL called:", response.url)
#         print("Foursquare status code:", response.status_code)

#         if response.status_code != 200:
#             print("Foursquare raw response:", response.text)

#             return {
#                 "error": f"Foursquare API failed with status code {response.status_code}",
#                 "details": response.text,
#                 "hotels": []
#             }

#         data = response.json()
#         results = data.get("results", [])

#         hotels = []

#         for item in results:
#             location = item.get("location") or {}
#             categories = item.get("categories") or []

#             category_names = []

#             for category in categories:
#                 category_name = category.get("name")
#                 if category_name:
#                     category_names.append(category_name)

#             hotels.append({
#                 "name": item.get("name") or "Unknown hotel",
#                 "address": (
#                     location.get("formatted_address")
#                     or location.get("address")
#                     or "Address not available"
#                 ),
#                 "categories": category_names,
#                 "price": item.get("price"),
#                 "rating": item.get("rating"),
#                 "distance": item.get("distance"),
#                 "fsq_id": (
#                     item.get("fsq_place_id")
#                     or item.get("fsq_id")
#                     or item.get("id")
#                 )
#             })

#         return {
#             "hotels": hotels
#         }

#     except Exception as e:
#         print("[Foursquare Service] Error:", e)

#         return {
#             "error": str(e),
#             "hotels": []
#         }


# def format_hotel_suggestions(hotels: list) -> str:
#     """
#     Converts Foursquare hotel results into readable text.

#     This does not invent hotel prices.
#     If price is not provided by Foursquare, it says price is not available.
#     """

#     if not hotels:
#         return "Hotel suggestions are not available."

#     hotel_text = "Suggested hotel options from Foursquare:\n\n"

#     for index, hotel in enumerate(hotels, start=1):
#         name = hotel.get("name") or "Unknown hotel"
#         address = hotel.get("address") or "Address not available"
#         categories = hotel.get("categories") or []
#         price = hotel.get("price")
#         rating = hotel.get("rating")
#         distance = hotel.get("distance")

#         category_text = ", ".join(categories) if categories else "Hotel / Accommodation"

#         hotel_text += f"{index}. {name}\n"
#         hotel_text += f"   Area/Address: {address}\n"
#         hotel_text += f"   Type: {category_text}\n"

#         if price:
#             hotel_text += f"   Price info from Foursquare: {price}\n"
#         else:
#             hotel_text += "   Price info from Foursquare: Not available\n"

#         if rating:
#             hotel_text += f"   Rating: {rating}\n"

#         if distance:
#             hotel_text += f"   Distance: {distance} meters from searched location\n"

#         hotel_text += "\n"

#     return hotel_text.strip()