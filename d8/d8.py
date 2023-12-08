from __future__ import annotations
from dataclasses import dataclass
from typing import List
from typing import Dict
from typing import Tuple

@dataclass
class Trip:
    location: str
    map: Map

    def walk(self) -> List[Tuple[str, str]]:
        path: List[Tuple[str, str]] = []

        arrived: bool = False

        while not arrived:
            for i in range(0, len(map.directions)):
                node: Node = map.nodes[self.location]
                next_node: str = node.left if map.directions[i] == "L" else node.right

                self.location = next_node

                path.append((map.directions[i], self.location))

                if self.location == "ZZZ":
                    arrived = True
                    break

        return path
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

if __name__ == "__main__":
    with open("input.txt") as data_file:
        map: Map = Map.parse(data_file.readlines())
        trip: Trip = Trip("AAA", map)

        steps: List[Tuple[str, str]] = trip.walk()

        print(steps)
        print(len(steps))