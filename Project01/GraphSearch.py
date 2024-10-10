# Kyle Tranfaglia
# COSC411 - Project01
# Last updated 10/09/24
# This program uses a BFS, DFS, and UCS algorithm to find a path given a start
# city and destination city in the provided undirected & weighted graph

import time
from collections import deque
from queue import PriorityQueue

# Undirected city graph with distances (miles) in alphabetical order with shortest to the longest paths (edges)
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

    # Queue (doubled-ended | FIFO) for BFS that stores a tuple: (current city, path so far, total distance traveled)
    queue = deque([(start, [start], 0)])
    # List to track visited cities and prevent revisits & infinite loops
    visited = []

    # Continue search as long as there are cities in the queue left to explore
    while (queue):
        # Remove first city from queue (FIFO) and store the tuple individually | O(1) compared to O(n) for .pop(0)
        city, path, distance = queue.popleft()

        # Check if destination has been reached
        if (city == destination):
            # End timer and calculate time taken to complete search
            end_time = time.perf_counter()
            time_taken = end_time - start_time

            # Print results from BFS
            print("\nBFS Path:")
            print(f"Path: {' -> '.join(path)}")  # join list elements of path into a single string separated by ->
            print(f"Total distance: {distance} miles")
            print(f"Time taken: {time_taken:.7f} seconds")

            return
        else:
            # Explore all neighboring cities if not already visited
            for neighbor, miles in graph[city].items():
                # Check if a neighbor has been visited, then add it to the queue with an updated path and total distance
                if (neighbor not in visited):
                    queue.append((neighbor, path + [neighbor], distance + miles))

            visited.append(city)  # Add current city to set to avoid revisit

    # Since the graph is connected, this should never happen with valid input: displays message on a failed search
    print(f"No path found from {start} to {destination}")


# Depth First Search algorithm to finds a path (leftmost | first found) between a start and end city
def dfs(graph, start, destination):
    start_time = time.perf_counter()  # Start timer

    # Stack (LIFO) for DFS that stores a tuple: (current city, path so far, total distance traveled)
    stack = [(start, [start], 0)]
    # List to track visited cities and prevent revisits & infinite loops
    visited = []

    # Continue search as long as there are cities in the stack left to explore
    while (stack):
        # Remove first city from queue (FIFO) and store the tuple individually | O(1) compared to O(n) for .pop(0)
        city, path, distance = stack.pop()

        # Check if destination has been reached
        if (city == destination):
            # End timer and calculate time taken to complete search
            end_time = time.perf_counter()
            time_taken = end_time - start_time

            # Print results from DFS
            print("\nDFS Path:")
            print(f"Path: {' -> '.join(path)}")  # join list elements of path into a single string separated by ->
            print(f"Total distance: {distance} miles")
            print(f"Time taken: {time_taken:.7f} seconds")

            return
        else:
            # Explore all neighboring cities if not already visited
            for neighbor, miles in graph[city].items():
                # Check if a neighbor has been visited, then add it to the stack with an updated path and total distance
                if (neighbor not in visited):
                    stack.append((neighbor, path + [neighbor], distance + miles))

            visited.append(city)  # Add current city to set to avoid revisit

    # Since the graph is connected, this should never happen with valid input: displays message on a failed search
    print(f"No path found from {start} to {destination}")


# Uniform Cost Search algorithm to finds the optimal (the least cost) path between a start and end city
def ucs(graph, start, destination):
    start_time = time.perf_counter()  # Start timer

    # Priority queue for UCS that stores a tuple: (total distance traveled *priority item*, current city, path so far)
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, [start]))  # Initialize with the start city and distance as 0 (distance is priority)

    # Dictionary to track the least cost to reach each city
    visited = {}

    # Continue search as long as there are cities in the priority queue left to explore
    while (not priority_queue.empty()):
        # Get the city with the lowest cost from the priority queue and store the tuple individually
        distance, city, path = priority_queue.get()

        # Check if destination has been reached
        if (city == destination):
            # End timer and calculate time taken to complete search
            end_time = time.perf_counter()
            time_taken = end_time - start_time

            # Print results from DFS
            print("\nUCS Path:")
            print(f"Path: {' -> '.join(path)}")  # join list elements of path into a single string separated by ->
            print(f"Total distance: {distance} miles")
            print(f"Time taken: {time_taken:.7f} seconds")

            return
        else:
            # Visit the city if not yet visited or revisit if a smaller distance (ensure optimality) is found
            if (city not in visited or distance < visited[city]):
                visited[city] = distance  # Set the minimum cost to reach this city

                # Explore all neighboring cities
                for neighbor, miles in graph[city].items():
                    new_distance = distance + miles  # Calculate the new total distance (cost) to reach the neighbor

                    # Check if it's a new city or has a lower cost and add the neighbor to the priority queue
                    if (neighbor not in visited or new_distance < visited[neighbor]):
                        priority_queue.put((new_distance, neighbor, path + [neighbor]))

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


# Driver program (main)
if (__name__ == "__main__"):
    # Program welcome message
    print("Find a path from city x to city y using the following: Baltimore, "
          "Boston, Buffalo, New York, Norfolk, Philadelphia, Pittsburgh, Richmond, Salisbury, Washington DC")

    # Get and validate user input for the start and destination city
    start_city = get_city_input("Enter the start city: ", city_graph)
    destination_city = get_city_input("Enter the destination city: ", city_graph)

    # Call BFS function to find & display the shortest path (the least cities traveled)
    bfs(city_graph, start_city, destination_city)

    # Call DFS function to find & display a path (leftmost | first found)
    dfs(city_graph, start_city, destination_city)

    # Call UCS function to find & display the optimal path (the lowest cost/distance)
    ucs(city_graph, start_city, destination_city)
