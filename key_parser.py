import re

pattern = re.compile('([0-9]*x)\[(.*)\]D=(.*)P=(.*)')


def parse_line(line):
    line = line.replace(" ", "")
    m = pattern.match(line)
    record = {
        "rounds": m.group(1),
        "lin_prop": m.group(2),
        "D": list(map(lambda x: int(x), m.group(3).replace(",", " ").strip().split(" "))),
        "P": list(map(lambda x: int(x), m.group(4).replace(",", " ").strip().split(" ")))
    }
    return record


def parse_file(file='T310_LC1RweakKT1.keys.txt'):
    aggregate = []
    category_map = {}
    with open(file, 'r') as input:
        for line in input.readlines():
            l = parse_line(line)
            aggregate.append(l)
            key = l["rounds"] + l["lin_prop"]
            if key in category_map:
                category_map[key].append(l)
            else:
                category_map[key] = [l]
    return aggregate, category_map


if __name__ == "__main__":
    print(parse_file())
