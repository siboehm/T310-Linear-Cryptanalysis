#! python2.7
from argon import ARGON
import random
from key_parser import parse_file


# computes XOR on the given array elements
def xor(arr):
    return reduce(lambda res, el: res != el, arr)


# returns array containing only the elements at the specified indices
def filter_by_index(arr, indices):
    return [x for x, i in zip(arr, range(len(arr))) if i in indices]


random.seed(123)
NUM_ITER = 5

long_term_key = {"alpha": 123, "D": [], "P": []}
IV = [0 for _ in range(61)]
s1 = [0 for _ in range(120)]
s2 = [0 for _ in range(120)]

theorems = parse_file()[0]
broken = 0
for theorem in theorems:
    long_term_key["D"] = [None] + theorem["D"]
    long_term_key["P"] = [None] + theorem["P"]

    # setup the cypher
    enc = ARGON(long_term_key, IV, s1, s2)

    for _ in range(NUM_ITER):
        # generate some new input
        u = [None] + [int(i) for i in format(random.getrandbits(36), '0>36b')]

        # feed input to cypher
        enc.settings["u0"] = u
        enc.reset()

        input_xor = xor(filter_by_index(u, theorem["lin_prop"]))

        # run the cypher
        output = enc.u(theorem["rounds"])
        output_xor = xor(filter_by_index(output, theorem["lin_prop"]))

        if input_xor != output_xor:
            broken += 1
            # print theorem
            break

print "broken:", broken, "num:", len(theorems)
