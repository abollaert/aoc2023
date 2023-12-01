def read_data(data_file):
    with open(data_file) as f:
        return f.read().splitlines()

def get_calibration_value(data):
    numbers = []

    for index, c in enumerate(data):
        if c.isnumeric():
            numbers.append(int(c))
        else:
            if c == "z" and index < len(data) - 3 and data[index + 1] == "e" and data[index + 2] == "r" and data[index + 3] == "o":
                numbers.append(0)
            elif c == "o" and index < len(data) - 2 and data[index + 1] == "n" and data[index + 2] == "e":
                numbers.append(1)
            elif c == "t" and index < len(data) - 2 and data[index + 1] == "w" and data[index + 2] == "o":
                numbers.append(2)
            elif c == "t" and index < len(data) - 4 and data[index + 1] == "h" and data[index + 2] == "r" and data[index + 3] == "e" and data[index + 4] == "e":
                numbers.append(3)
            elif c == "f" and index < len(data) - 3 and data[index + 1] == "o" and data[index + 2] == "u" and data[index + 3] == "r":
                numbers.append(4)
            elif c == "f" and index < len(data) - 3 and data[index + 1] == "i" and data[index + 2] == "v" and data[index + 3] == "e":
                numbers.append(5)
            elif c == "s" and index < len(data) - 2 and data[index + 1] == "i" and data[index + 2] == "x":
                numbers.append(6)
            elif c == "s" and index < len(data) - 4 and data[index + 1] == "e" and data[index + 2] == "v" and data[index + 3] == "e" and data[index + 4] == "n":
                numbers.append(7)
            elif c == "e" and index < len(data) - 4 and data[index + 1] == "i" and data[index + 2] == "g" and data[index + 3] == "h" and data[index + 4] == "t":
                numbers.append(8)
            elif c == "n" and index < len(data) - 3 and data[index + 1] == "i" and data[index + 2] == "n" and data[index + 3] == "e":
                numbers.append(9)

    if len(numbers) == 0:
        return None

    return numbers[0] * 10 + numbers[len(numbers) - 1]

data = read_data("input1.txt")
numbers = list(map(get_calibration_value, data))

print(sum(numbers))
