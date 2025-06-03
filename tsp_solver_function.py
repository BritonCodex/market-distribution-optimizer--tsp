#Responsibility: Define the function that solves the TSP using brute-force.

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
