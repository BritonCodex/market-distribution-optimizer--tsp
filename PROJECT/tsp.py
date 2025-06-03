# Traveling Salesman Problem (TSP) Route Optimizer in Kenya

# --- Imports ---
import openrouteservice  # For accessing OpenRouteService API for geocoding and routing
from openrouteservice.distance_matrix import distance_matrix  # For fetching distance matrices
import itertools         # For generating route permutations (TSP brute-force)
import folium            # For interactive map visualization
import webbrowser        # To open the generated map in a browser
import sys  
import os
from  dotenv import load_dotenv  # For loading environment variables from .env file
# --- Environment Setup ---
# Ensure you have the required packages installed:
load_dotenv()


# Replace the API key below with your own OpenRouteService key if needed.
ORS_API_KEY = os.getenv("ORS_API_KEY")  # Ensure you have set this environment variable
if not ORS_API_KEY:
    sys.exit("❌ Please set the ORS_API_KEY environment variable with your OpenRouteService API key.")
client = openrouteservice.Client(key=ORS_API_KEY)

load_dotenv()

# --- User Input: Town Names ---
print("🛣️ Enter town names separated by commas (e.g., Nairobi, Meru, Nyeri ,Muranga , Thika,,  Ruiru):")
input_towns = input("📍 Towns: ").split(',')
# Clean and standardize town names (strip whitespace, capitalize)
town_names = [t.strip().title() for t in input_towns if t.strip()] #Standardize names and remove empty entries  whitespace and capitalize them

# --- Input Validation ---
if len(town_names) < 2:# ensures atleast 2 towns are provided
    sys.exit("❌ Please enter at least two towns.")  # Need at least two towns for TSP

if len(town_names) > 10:# maximum threshold of towns
    print("⚠️ Warning: Too many towns. This could take a long time due to TSP complexity (factorial time).")

# --- User Input: Starting Town Selection ---
print("\n🎯 Choose starting town from the list below:")
for i, town in enumerate(town_names):#lists the towns down vertically
    print(f"{i+1}. {town}")
try:
    start_index = int(input("➡️ Enter the number of the starting town: ")) - 1 #this depicts the starting town
    if not 0 <= start_index < len(town_names):
        raise ValueError
except ValueError:
    sys.exit("❌ Invalid input. Please enter a valid number from the list.")

# Assign the starting town based on user selection
start = town_names[start_index]

# -------- COORDINATE LOOKUP --------
def get_coordinates(place_name):
    try:
        result = client.pelias_search(text=place_name + ", Kenya", size=1)
        coords = result['features'][0]['geometry']['coordinates']
        return tuple(coords)
    except Exception as e:
        print(f"❌ Error for {place_name}: {e}")
        return None

print("\n📍 Fetching coordinates...")
locations = {}
for town in town_names:
    coords = get_coordinates(town)
    if coords:
        locations[town] = coords
    else:
        sys.exit(f"⚠️ Could not resolve coordinates for: {town}")

coordinates = [locations[t] for t in town_names]

# -------- DISTANCE MATRIX --------
print("\n🔄 Fetching real road distances from ORS...")
              
try:
    matrix = distance_matrix(client, locations=coordinates, profile='driving-car', metrics=['distance'], units='km')# asks for distsnces between locations while driving a car
except Exception as e:
    sys.exit(f"❌ Failed to fetch distance matrix: {e}") #stops the  program

raw_distances = matrix['distances']

distance_dict = {
    town_names[i]:  { #starting town i and destination town j
        town_names[j]: raw_distances[i][j] for j in range(len(town_names)) if i != j
    } for i in range(len(town_names)) #goes through every time
}

# -------- TSP SOLVER --------
def solve_tsp(start, towns, dist):
    min_dist = float('inf')
    best_route = []
    for perm in itertools.permutations([t for t in towns if t != start]):
        route = [start] + list(perm) + [start]
        total = sum(dist[route[i]][route[i+1]] for i in range(len(route) - 1))
        if total < min_dist:
            min_dist = total
            best_route = route
    return best_route, min_dist

route, total_km = solve_tsp(start, town_names, distance_dict)

# -------- PRINT RESULTS --------
print("\n✅ Optimal Delivery Route:")
for i, town in enumerate(route):
    print(f"{i+1}. {town}")
print(f"📏 Total Driving Distance: {total_km:.2f} km")

# -------- MAP DISPLAY --------
map_center = (locations[start][1], locations[start][0])
m = folium.Map(
    location=map_center,
    zoom_start=8,
    tiles="CartoDB positron"
)

# Add styled markers
for i, town in enumerate(route):
    lat, lon = locations[town][1], locations[town][0]
    if i == 0:
        folium.Marker(
            [lat, lon],
            tooltip="Start: " + town,
            popup=f"Start: {town}",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
    else:
        folium.Marker(
            [lat, lon],
            tooltip=f"Step {i+1}: {town}",
            popup=f"{i+1}. {town}",
            icon=folium.DivIcon(html=f"""<div style="font-size: 14pt; color: #0033cc;"><b>{i+1}</b></div>""")
        ).add_to(m)

# Draw straight lines for route
for i in range(len(route) - 1):
    from_town = route[i]
    to_town = route[i + 1]
    coords = [
        (locations[from_town][1], locations[from_town][0]),
        (locations[to_town][1], locations[to_town][0])
    ]
    dist_km = distance_dict[from_town][to_town]
    folium.PolyLine(
        coords,
        color="blue",
        weight=6,
        opacity=0.7,
        tooltip=f"{from_town} → {to_town}: {dist_km:.1f} km"
    ).add_to(m)

# Add legend
legend_html = f"""
<div style="
    position: fixed; bottom: 40px; left: 40px; width: 290px; height: auto;
    background-color: white; border: 2px solid #666; z-index: 9999;
    padding: 12px; font-size: 14px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
">
<b>🚚 Optimal Route:</b><br>
{" → ".join(route)}<br>
<b>Total Distance:</b> {total_km:.2f} km
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

map_file = "tsp_interactive_route.html"
m.save(map_file)
webbrowser.open(map_file)
print(f"\n🗺️ Clean map saved and opened: {map_file}")
