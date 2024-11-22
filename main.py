from keplergl import KeplerGl
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import pandas as pd

def get_coordinates(cities):
    """Получает координаты для списка городов."""
    geolocator = Nominatim(user_agent="city_locator")
    data = []
    for city in cities:
        try:
            location = geolocator.geocode(city, timeout=10)
            if location:
                data.append({"city": city, "latitude": location.latitude, "longitude": location.longitude})
            else:
                print(f"Coordinates for '{city}' not found.")
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Error fetching coordinates for '{city}': {e}")
    return data

def create_map(data):
    """Создает карту с помощью Kepler.gl."""
    df = pd.DataFrame(data)
    map_ = KeplerGl(height=600)
    map_.add_data(data=df, name="Cities")
    return map_

if __name__ == "__main__":
    # Получаем список городов от пользователя
    user_input = input("Enter city names (comma-separated): ").strip()
    cities = [city.strip() for city in user_input.split(",")]
    
    if not cities:
        print("No cities provided.")
    else:
        data = get_coordinates(cities)
        if data:
            map_ = create_map(data)
            # Сохраняем карту в HTML
            map_.save_to_html(file_name="cities_map.html")
            print("Map saved as 'cities_map.html'. Open it in your browser!")
        else:
            print("No valid coordinates to map.")
