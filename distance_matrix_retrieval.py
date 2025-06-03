#Responsibility: Use ORS to fetch the real road distances between all towns.

# -------- DISTANCE MATRIX --------
print("\n Fetching real road distances from ORS...")
try:
    matrix = distance_matrix(client, locations=coordinates, profile='driving-car', metrics=['distance'], units='km')
except Exception as e:
    sys.exit(f" Failed to fetch distance matrix: {e}")

raw_distances = matrix['distances']

distance_dict = {
    town_names[i]: {
        town_names[j]: raw_distances[i][j] for j in range(len(town_names)) if i != j
    } for i in range(len(town_names))
}
