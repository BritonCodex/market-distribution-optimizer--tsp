def get_coordinates(place_name):
    try:
        result = client.pelias_search(text=place_name + ", Kenya", size=1)
        coords = result['features'][0]['geometry']['coordinates']
        return tuple(coords)
    except Exception as e:
        print(f" Error for {place_name}: {e}")
        return None
