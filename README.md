
# 🚚 Optimal Delivery Route Planner for Kenyan Towns

This project is a Python-based delivery route optimizer that helps plan the shortest possible delivery route between multiple towns in Kenya using real road distances. It solves the **Traveling Salesman Problem (TSP)** and visualizes the route on an interactive map.

---

## 🔍 Overview

- Takes in town names and a selected starting point.
- Retrieves GPS coordinates via **OpenRouteService (ORS)**.
- Calculates road-based distances using ORS.
- Solves the TSP to find the shortest circular route.
- Displays the route interactively using **Folium**.

---

## 🎯 Objectives

- Accept user-inputted Kenyan towns.
- Automatically resolve geographic coordinates.
- Fetch accurate driving distances via API.
- Determine the shortest circular delivery route.
- Visualize the route interactively with total distance.

---

## 🛠️ Tools & Technologies

| Tool              | Use                                         |
|------------------|---------------------------------------------|
| `openrouteservice` | API for coordinates & driving distances   |
| `itertools`       | Route permutation logic                    |
| `folium`          | Interactive map generation                 |
| `webbrowser`      | Automatically open generated map file      |
| `Python 3.x`      | Core programming language                  |

---

## 🧩 Key Features

- ✅ Easy user input for towns and starting point
- 📍 Accurate coordinates from OpenRouteService
- 🔁 Brute-force TSP solver for ≤10 towns
- 🗺️ Folium-based interactive route map
- 📏 Displays total driving distance
- 💾 Automatically saves and opens HTML map file

---

## 🔄 How It Works

1. **Input Phase**: User enters town names and selects a starting town.
2. **Geocoding**: Coordinates are fetched for each town.
3. **Distance Matrix**: Road distances between towns are retrieved.
4. **Route Solver**: All permutations are evaluated for shortest path.
5. **Map Visualization**: Route is plotted with numbered markers and lines.

---

## 📊 Example

```plaintext
🛣️ Towns: Nairobi, Nakuru, Eldoret, Kisumu
🎯 Starting Point: Nairobi

✅ Optimal Route:
1. Nairobi
2. Nakuru
3. Eldoret
4. Kisumu
5. Nairobi

📏 Total Distance: 745.20 km
🗺️ Output: tsp_interactive_route.html
```

---

## 🔐 API Key

This project requires an OpenRouteService API key.

- Sign up at: https://openrouteservice.org/dev/#/signup
- Replace the placeholder key in your script:

```python
client = openrouteservice.Client(key='your-api-key-here')
```

---

## ⚠️ Limitations

| Limitation          | Description                               |
|---------------------|-------------------------------------------|
| TSP Brute-force     | Not scalable beyond 10 towns              |
| Straight lines      | Routes on map are not actual road paths   |
| Internet dependency | Requires internet for API calls           |

---

## 📈 Future Enhancements

- Use ORS directions API for real road lines.
- GUI with Streamlit or Tkinter.
- Support for CSV/Excel input.
- Integrate with Google OR-Tools for large routes.

---

## 📂 Output

- Map file saved as `tsp_interactive_route.html`
- Open in any browser or share with teams easily

---

## 👨‍💻 Author & License

This tool was developed for educational and logistical optimization purposes in Kenya. Free for educational use. Please respect the usage limits and terms of OpenRouteService.

---

## 🧭 Related Links

- [OpenRouteService API Docs](https://openrouteservice.org/dev/#/)
- [OpenRouteService Python SDK](https://github.com/GIScience/openrouteservice-py)
- [Folium Documentation](https://python-visualization.github.io/folium/)
