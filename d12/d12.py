from dataclasses import dataclass
from typing import Tuple
from typing import List
from functools import cache

@dataclass
class Springs:
    springs: str
    groups: List[int]
    
@cache
def count_valid_patterns(groups: Tuple[int, ...], pattern: str) -> int:
    if len(groups) == 0:
        if "#" in pattern:
            return 0

        return 1

    current_group: int = groups[0]
    matching_patterns: int = 0

    for i in range(len(pattern) - sum(groups[1:])):
        for j in range(i, i + current_group):
            if j >= len(pattern):
                return matching_patterns

            if pattern[j] == ".":
                break
                
            if j == i and j > 0 and pattern[j - 1] == "#":
                return matching_patterns

            if j == i + current_group - 1:
                if j + 1 < len(pattern) and pattern[j + 1] == "#":
                    break

                matching_patterns += count_valid_patterns(groups[1:], pattern[j + 2 :])

    return matching_patterns

def parse_line(line: str) -> Springs:
    parts: List[str] = line.split()

    springs: str = parts[0]
    expanded: str = ""

    for i in range(0, 5):
        expanded = expanded + springs

        if i < 4:
            expanded = expanded + "?"

    groups: List[int] = [int(x) for x in parts[1].split(",")]

    expanded_groups: List[int] = []

    for i in range(0, 5):
        expanded_groups.extend(groups)

    #print("Expanded : springs %s, groups %s" % (expanded, expanded_groups))
    return Springs(expanded, expanded_groups)

if __name__ == "__main__":
    springs: List[Springs] = []

    with open("input.txt") as data_file:
        for line in data_file.readlines():
            springs.append(parse_line(line))

    total: int = 0

    for spring in springs:
        total = total + count_valid_patterns(tuple(spring.groups), spring.springs)

    print(total)




