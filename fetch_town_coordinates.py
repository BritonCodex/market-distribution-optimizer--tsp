#Responsibility: Use the function to get coordinates for each town and validate.

print("\n Fetching coordinates...")
locations = {}
for town in town_names:
    coords = get_coordinates(town)
    if coords:
        locations[town] = coords
    else:
        sys.exit(f" Could not resolve coordinates for: {town}")

coordinates = [locations[t] for t in town_names]
