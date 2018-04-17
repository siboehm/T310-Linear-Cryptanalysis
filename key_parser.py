import re
import sys

pattern = re.compile('([0-9]*x)\[(.*)\]D=(.*)P=(.*)')


def _parse_lin_prop(string):
    result = []

    if len(string) == 0:
        raise ValueError("Invalid entry, array of indices can't be empty")

    lin_props = string.split(",")

    for lp in lin_props:
        if "-" in lp:
            a, b = [int(x) for x in lp.split("-")]
            result += list(range(a, b + 1))
        else:
            result += [int(lp)]

    return result


def parse_line(line):
    line = line.replace(" ", "")
    m = pattern.match(line)
    record = {
        "rounds": int(m.group(1)[:-1]),
        "lin_prop": _parse_lin_prop(m.group(2)),
        "D": list(
            map(lambda x: int(x),
                m.group(3).replace(",", " ").strip().split(" "))),
        "P": list(
            map(lambda x: int(x),
                m.group(4).replace(",", " ").strip().split(" ")))
    }
    return record


def parse_file(file='T310_LC1RweakKT1.keys.txt'):
    aggregate = []
    category_map = {}
    with open(file, 'r') as input:
        for line in input.readlines():
            l = parse_line(line)
            aggregate.append(l)
            key = str(l["rounds"]) + str(l["lin_prop"])
            if key in category_map:
                category_map[key].append(l)
            else:
                category_map[key] = [l]
    return aggregate, category_map


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print parse_file(sys.argv[1])
    else:
        print parse_file()
