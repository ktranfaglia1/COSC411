# Kyle Tranfaglia
# COSC411 - Project01
# Last updated 10/09/24
# This program uses a BFS, DFS, and UCS algorithm to find a path given a start
# city and destination city in the provided undirected & weighted graph

import time
from collections import deque

# Undirected city graph with distances (miles) in alphabetical order with shortest to longest paths (edges)
city_graph = {
    'Baltimore': {'Washington DC': 45, 'Salisbury': 117, 'Philadelphia': 101, 'Pittsburgh': 248},
    'Boston': {'New York': 216, 'Buffalo': 450},
    'Buffalo': {'Pittsburgh': 219, 'Boston': 450},
    'New York': {'Philadelphia': 94, 'Boston': 216, 'Pittsburgh': 370},
    'Norfolk': {'Richmond': 93, 'Salisbury': 132},
    'Philadelphia': {'New York': 94, 'Baltimore': 101, 'Salisbury': 138, 'Pittsburgh': 304},
    'Pittsburgh': {'Buffalo': 219, 'Baltimore': 248, 'Philadelphia': 304, 'New York': 370},
    'Richmond': {'Washington DC': 110, 'Norfolk': 93},
    'Salisbury': {'Baltimore': 117, 'Philadelphia': 138, 'Washington DC': 116, 'Norfolk': 132},
    'Washington DC': {'Baltimore': 45, 'Salisbury': 116, 'Richmond': 110}
}


# Breadth First Search algorithm to find the shortest path (the least cities traveled) between a start and end city
def bfs(graph, start, destination):
    start_time = time.perf_counter()  # Start timer

    # Queue (doubled-ended) for BFS (current city, path so far, total distance traveled)
    queue = deque([(start, [start], 0)])
    # Set to track visited cities and prevent revisits & infinite loops
    visited = set()

    # Continue search as long as there are cities in the queue left to explore
    while (queue):
        city, path, distance = queue.popleft()  # Remove first city from queue (FIFO) and store the tuple individually

        if (city == destination):
            # End timer and calculate time taken to complete search
            end_time = time.perf_counter()
            time_taken = end_time - start_time

            # Print results from BFS
            print(f"\nPath: {' -> '.join(path)}")  # join list elements of path into a single string separated by ->
            print(f"Total distance: {distance} miles")
            print(f"Time taken: {time_taken:.7f} seconds")
            return
        else:
            # Explore all neighboring cities if not already visited
            for neighbor, miles in graph[city].items():
                # Check if a neighbor has been visited, then add it to the queue with an updated path and total distance
                if (neighbor not in visited):
                    queue.append((neighbor, path + [neighbor], distance + miles))

            visited.add(city)  # Add current city to set to avoid revisit

    # Since the graph is connected, this should never happen with valid input: displays message on a failed search
    print(f"No path found from {start} to {destination}")


# Get and validate user input until a city in the graph is entered
def get_city_input(prompt, graph):
    city = input(prompt).strip()  # Get for input and strip any surrounding whitespace

    # Prompt for a city until a valid city (in the graph) is entered
    while (city not in graph):
        print(f"'{city}' is not in the graph. Please enter a valid city.")
        city = input(prompt).strip()  # Get for input and strip any surrounding whitespace

    return city


# Driver program
if __name__ == "__main__":
    # Program welcome message
    print("Find a path from city x to city y using the following: Baltimore, "
          "Boston, Buffalo, New York, Norfolk, Philadelphia, Pittsburgh, Richmond, Salisbury, Washington DC")

    # Get and validate user input for the start and destination city
    start_city = get_city_input("Enter the start city: ", city_graph)
    destination_city = get_city_input("Enter the destination city: ", city_graph)

    # Call BFS function to find & display the shortest path (the least cities traveled)
    bfs(city_graph, start_city, destination_city)
