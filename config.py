# Author : Om "Ethcelon" Bhallamudi
# Version : 1.b1
# LONG TERM SECRETS
D=[None,0,28,4,32,24,8,12,20,16]
P=[None,8,4,33,16,31,20,5,35,9,3,19,18,12,7,21,13,23,25,28,36,24,15,26,29,27,32,11]

KeyDict = {
# TODO /key26 # default to 26 - Option to be implemented!
   17: [[None, 22, 23, 33, 11, 26, 12, 5, 4, 9, 3, 2, 1, 19, 21, 10, 8, 7, 25, 6, 35, 32, 31, 30, 29, 17, 17, 34],
        [None, 0, 4, 8, 12, 16, 20, 24, 28, 32]],
   14: [[None, 24, 34, 33, 32, 14, 4, 5, 28, 9, 26, 27, 18, 36, 16, 21, 15, 20, 25, 35, 8, 1, 6, 23, 29, 19, 12, 13],
        [None, 0, 28, 24, 12, 16, 32, 36, 4, 20]],
   26: [[None, 8, 4, 33, 16, 31, 20, 5, 35, 9, 3, 19, 18, 12, 7, 21, 13, 23, 25, 28, 36, 24, 15, 26, 29, 27, 32, 11],
        [None, 0, 28, 4, 32, 24, 8, 12, 20, 16]],
   15: [[None, 15, 13, 33, 34, 6, 8, 5, 3, 9, 18, 14, 22, 28, 30, 21, 31, 7, 25, 26, 16, 27, 11, 23, 29, 19, 1, 36],
        [None, 0, 4, 17, 12, 35, 32, 2, 24, 20]],
   16: [[None, 14, 19, 33, 18, 23, 15, 5, 6, 9, 2, 34, 1, 30, 11, 21, 3, 22, 25, 17, 7, 32, 10, 27, 29, 26, 35, 13],
        [None, 0, 35, 19, 23, 27, 11, 3, 15, 31]],
   21: [[None, 36, 4, 33, 11, 1, 20, 5, 26, 9, 24, 32, 7, 12, 2, 21, 3, 28, 25, 34, 8, 31, 13, 18, 29, 16, 19, 6],
       [None,0, 24, 36, 4, 16, 28, 12, 20, 32]],
   30: [[None,8, 28, 33, 3, 27, 20, 5, 16, 9, 1, 19, 23, 4, 2, 21, 36, 30, 25, 11, 24, 12, 18, 7, 29, 32, 6, 35],
       [None,0, 36, 8, 28, 12, 32, 4, 20, 16]],
   32:[[None,27, 30, 33, 24, 11, 36, 5, 20, 9, 23, 1, 34, 16, 14, 21, 8, 28, 25, 22, 32, 4, 10, 13, 29, 15, 12, 18],
       [None,0, 20, 24, 4, 28, 8, 16, 36, 12]],
   33:[[None,24, 3, 33, 30, 2, 8, 5, 12, 9, 1, 10, 6, 32, 22, 21, 18, 28, 25, 16, 20, 36, 13, 17, 29, 26, 4, 35],
       [None,0, 12, 24, 36, 28, 16, 32, 8, 4]],
}

#F = get_deterministic_iv()

# KEY BITS
s1 = [0 for i in range(120)]
s2 = [0 for i in range(120)]

long_term_key = {
    "alpha" : 23,
    "D" : D,
    "P" : P,
}

default_args = {
    'rounds' : 1,
    'ins' : [1],
    'fix' : [0],
    'sat' : False,
    'xl' : False,
}
