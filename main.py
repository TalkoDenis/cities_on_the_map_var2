from keplergl import KeplerGl
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def get_coordinates_for_city(city, geolocator):
    try:
        location = geolocator.geocode(city, timeout=10)
        if location:
            return {"city": city, "latitude": location.latitude, "longitude": location.longitude}
        else:
            print(f"Coordinates for '{city}' not found.")
            return None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Error fetching coordinates for '{city}': {e}")
        return None

def get_coordinates(cities):
    geolocator = Nominatim(user_agent="city_locator")
    data = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda city: get_coordinates_for_city(city, geolocator), cities)
        data = [result for result in results if result is not None]
    return data

def create_map(data, center_coordinates=(44.8176, 20.4633)):
    """Create the map with center in Belgrade"""
    df = pd.DataFrame(data)
    map_kepler = KeplerGl(height=600)
    if not df.empty:
        map_kepler.add_data(data=df, name="Cities")
    map_kepler.config = {
        "visState": {
            "mapState": {
                "latitude": center_coordinates[0],
                "longitude": center_coordinates[1],
                "zoom": 6
            }
        }
    }
    return map_kepler

if __name__ == "__main__":
    user_input = input("Enter city names (comma-separated): ").strip()
    cities = [city.strip() for city in user_input.split(",")]

    if not cities:
        print("No cities provided. Displaying map centered at Belgrade.")
        data = []
    else:
        data = get_coordinates(cities)

    if data:
        map_kepler = create_map(data)
        map_kepler.save_to_html(file_name="cities_map_kepler.html")
        print("Map saved as 'cities_map_kepler.html'.")
    else:
        map_kepler = create_map(data)
        map_kepler.save_to_html(file_name="cities_map_kepler.html")
        print("No valid coordinates to map. Map centered at Belgrade saved as 'cities_map_kepler.html'.")
