from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Dict
from math import lcm

@dataclass
class Trip:
    start_locations: List[str] = field(init=False)
    locations: List[str] = field(init=False)
    steps_to_reach_end: Dict[str, int] = field(init=False)
    map: Map

    def walk(self) -> int:
        self.locations = self.map.find_start_points()
        self.start_locations = self.locations
        self.steps_to_reach_end = {}

        for location in self.locations:
            self.steps_to_reach_end[location] = 0

        print("Map has %d starting points." % (len(self.locations)))

        arrived: bool = False
        num_steps: int = 0

        while not arrived:
            for i in range(0, len(map.directions)):
                arrived = self.__step(map.directions[i])
                num_steps = num_steps + 1

                if arrived:
                    break

        return lcm(*self.steps_to_reach_end.values())

    def __step(self, direction: str) -> bool:
        new_locations: List[Node] = []

        for i in range(0, len(self.locations)):
            current_location: str = self.locations[i]

            if not self.map.nodes[current_location].is_end_node():
                start_location: str = self.start_locations[i]

                node: Node = map.nodes[current_location]
                next_node = self.map.nodes[node.left] if direction == "L" else self.map.nodes[node.right]

                new_locations.append(next_node)

                self.steps_to_reach_end[start_location] = self.steps_to_reach_end[start_location] + 1
            else:
                new_locations.append(self.map.nodes[current_location])

        self.locations = [location.name for location in new_locations]

        for i in range(0, len(new_locations)):
            new_location = new_locations[i]

            if not new_location.is_end_node():
                return False

        return True

@dataclass
class Node:
    name: str
    left: str
    right: str

    @staticmethod
    def parse(line: str) -> Node:
        parts: List[str] = line.split("=")

        name: str = parts[0].strip()

        next_parts = parts[1].split(",")

        left: str = next_parts[0].replace("(", "").strip()
        right: str = next_parts[1].replace(")", "").strip()

        return Node(name, left, right)

    def is_start_node(self):
        return self.name.endswith("A")

    def is_end_node(self):
        return self.name.endswith("Z")

@dataclass
class Map:
    directions: List[str]
    nodes: Dict[str, Node]

    @staticmethod
    def parse(data_lines: List[str]) -> Map:
        directions: List[str] = []
        nodes: Dict[str, Node] = {}

        for direction in data_lines[0].strip():
            directions.append(direction)

        for line in data_lines[2:]:
            n: Node = Node.parse(line)

            nodes[n.name] = n

        return Map(directions, nodes)

    def find_start_points(self) -> List[str]:
        start_points: List[str] = []

        for node in self.nodes.values():
            if node.is_start_node():
                start_points.append(node.name)

        return start_points

if __name__ == "__main__":
    with open("input.txt") as data_file:
        map: Map = Map.parse(data_file.readlines())
        trip: Trip = Trip(map)

        steps: int = trip.walk()

        print(steps)