from dataclasses import dataclass
from typing import Tuple
from typing import List
from typing import Set

@dataclass
class Springs:
    springs: str
    groups: List[int]

def find_groups(line: str) -> List[int]:
    groups: List[int] = []
    current_group: int = 0

    for c in line:
        if c == "#":
            current_group = current_group + 1
        elif c == ".":
            if current_group > 0:
                groups.append(current_group)
                current_group = 0

    if current_group != 0:
        groups.append(current_group)

    return groups

def matches(candidate: str, groups: List[int]) -> bool:
    groups_in_candidate: List[int] = find_groups(candidate)
    #print("Groups in candidate : %s, expected groups : %s" % (groups_in_candidate, groups))
    return groups_in_candidate == groups


def generate_candidates(line: str) -> Set[str]:
    candidates: Set[str] = set()

    if line.count("?") == 0:
        candidates.add(line)
    elif line.count("?") == 1:
        candidates.add(line.replace("?", "#"))
        candidates.add(line.replace("?", "."))
    else:
        next_candidates: Set[str] = generate_candidates(line.replace("?", "#", 1))

        for candidate in next_candidates:
            candidates.add(candidate)

        next_candidates: Set[str] = generate_candidates(line.replace("?", ".", 1))

        for candidate in next_candidates:
            candidates.add(candidate)

    return candidates

def parse_line(line: str) -> Springs:
    parts: List[str] = line.split()

    springs: str = parts[0]
    groups: List[int] = [int(x) for x in parts[1].split(",")]

    return Springs(springs, groups)

if __name__ == "__main__":
    springs: List[Springs] = []

    with open("input.txt") as data_file:
        for line in data_file.readlines():
            springs.append(parse_line(line))

    sum: int = 0

    for spring in springs:
        candidates: Set[str] = generate_candidates(spring.springs)
        matching_candidates: List[str] = [c for c in candidates if matches(c, spring.groups)]

        print("Matching candidates : %s" % (matching_candidates))

        sum = sum + len(matching_candidates)

    print(sum)



