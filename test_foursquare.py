from services.hotelsearch_service import get_hotels


result = get_hotels("Goa")

print("\nHOTEL RESULT:")
print(result)

print("\nFORMATTED HOTEL LIST:")

if result:
    for index, hotel in enumerate(result, start=1):
        print(f"{index}. {hotel.get('name', 'Unknown hotel')}")
        print(f"   Address: {hotel.get('address', 'Address not available')}")
else:
    print("No hotels found or Foursquare API failed.")