#! python2.7
from argon import ARGON
import random
from key_parser import parse_file


# computes XOR on the given array elements
def xor(arr):
    return reduce(lambda res, el: res != el, arr)


def filter_by_index(arr, indices):
    return [x for x, i in zip(arr, range(len(arr))) if i in indices]


# setting an arbitrary random key
long_term_key = {
    "alpha": 23,
    "D": [None, 0, 4, 20, 8, 32, 12, 24, 16, 28],
    "P": [
        None, 8, 20, 33, 31, 17, 16, 5, 19, 9, 2, 18, 28, 24, 1, 21, 11, 3, 25,
        4, 36, 12, 22, 15, 29, 23, 32, 6
    ]
}
random.seed(123)
IV = [int(i) for i in format(random.getrandbits(61), '0>61b')]
st_key = [int(s) for s in format(random.getrandbits(240), '0>240b')]
s1, s2 = st_key[:120], st_key[120:]

theorems = parse_file()[0]
broken = 0
for theorem in theorems:
    long_term_key["D"] = [None] + theorem["D"]
    long_term_key["P"] = [None] + theorem["P"]

    enc = ARGON(long_term_key, IV, s1, s2)

    input_xor = xor(filter_by_index(enc.settings["u0"], theorem["lin_prop"]))
    output_xor = xor(
        filter_by_index(enc.u(theorem["rounds"]), theorem["lin_prop"]))

    if input_xor != output_xor:
        broken += 1

print "broken:", broken, "num", len(theorems)
