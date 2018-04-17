# Author : Om "Ethcelon" Bhallamudi
# Version : 1.b1
class ARGON:
    settings = None

    def __init__(self, long_term_key, F, s1, s2):
        self.settings = {
            "long_term_key": long_term_key,
            "F": F,
            "s1": s1,
            "s2": s2,
            "u0": [
                None, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1
            ],
        }
        self.reset()

    def get_settings(self):
        return self.settings

    def reset(self):
        """ Resets the cipher to initial state/settings. """

        self.long_term_key = self.settings["long_term_key"]
        self.s1 = self.settings["s1"]
        self.s2 = self.settings["s2"]
        self.F = self.settings["F"]

        self.Ustate = [self.settings["u0"]]
        self.u_iCounter = 0
        self.test_vectors = []

        self.current_round = 0
        self.current_instance = 0

    def get_test_vectors(self):
        return self.test_vectors

    def set_current_instance(self, i):
        self.current_instance = i
        return True

    def get_current_instance(self):
        return self.current_instance

    def set_current_round(self, i):
        self.current_round = i
        return True

    def get_current_round(self):
        return self.current_round

    def get_f(self, i):
        from helpers import ret_str

        def var_F(n):
            j = n
            return ret_str('F', '%04d' % (j), '%03d' % self.current_instance)

        test_vectors = []
        """ TODO docs """
        j = i + 60
        k = j
        while len(self.F) < k + 1:
            self.F.append(self.F[j - 61] ^ self.F[j - 60] ^ self.F[j - 59] ^
                          self.F[j - 56])

        test_vectors.append('{}={}'.format(var_F(j), self.F[j]))
        self.test_vectors += test_vectors
        return self.F[j]

    def Z(self, e1, e2, e3, e4, e5, e6, z_n=0):
        from codegen import rvar

        def var(v, n):
            return rvar(v, n, self.current_instance, self.current_round)

        def var_Z(v, n):
            return 'Z_{}_'.format(z_n) + var(v, n)

        e1_eq = var_Z('E', 1)
        e2_eq = var_Z('E', 2)
        e3_eq = var_Z('E', 3)
        e4_eq = var_Z('E', 4)
        e5_eq = var_Z('E', 5)
        e6_eq = var_Z('E', 6)

        test_vectors = []

        x1 = '{}={}'.format(e1_eq, e1)
        x2 = '{}={}'.format(e2_eq, e2)
        x3 = '{}={}'.format(e3_eq, e3)
        x4 = '{}={}'.format(e4_eq, e4)
        x5 = '{}={}'.format(e5_eq, e5)
        x6 = '{}={}'.format(e6_eq, e6)

        test_vectors += [x1, x2, x3, x4, x5, x6]

        a = e1 ^ e5 ^ e6
        x1 = '{}={}'.format(var_Z('H', 1), a)

        b = (e1 and e4) ^ (e2 and e3) ^ (e2 and e5) ^ (e4 and e5) ^ (e5 and e6)
        x2 = '{}={}'.format(var_Z('H', 2), b)

        c = (e1 and e3 and e4) ^ (e1 and e3 and e6) ^ (e1 and e4 and e5) ^ (
            e2 and e3 and e6) ^ (e2 and e4 and e6) ^ (e3 and e5 and e6)
        x3 = '{}={}'.format(var_Z('H', 3), c)

        d = (e1 and e2 and e3 and e4) ^ (e1 and e2 and e3 and e5) ^ (
            e1 and e2 and e5 and e6) ^ (e2 and e3 and e4 and e6)
        x4 = '{}={}'.format(var_Z('H', 4), d)

        e_ = (e4 and e2) ^ (e4 and e6)
        x5 = '{}={}'.format(var_Z('W', 1), e_)

        e = e_ and e1 and e3 and e5
        x6 = '{}={}'.format(var_Z('H', 5), e)

        x7 = '{}={}'.format(var('Z_O', z_n), a ^ b ^ c ^ d ^ e ^ 1)

        test_vectors += [x1, x2, x3, x4, x5, x6, x7]

        self.test_vectors += test_vectors

        return a ^ b ^ c ^ d ^ e ^ 1  # according to changes specified by Dr Courtois

    def Z2(self, e1, e2, e3, e4, e5, e6):

        a = e1 ^ e5 ^ e6
        b = (e1 and e4) ^ (e2 and e3) ^ (e2 and e5) ^ (e4 and e5) ^ (e5 and e6)
        c = (e1 and e3 and e4) ^ (e1 and e3 and e6) ^ (e1 and e4 and e5) ^ (
            e2 and e3 and e6) ^ (e2 and e4 and e6) ^ (e3 and e5 and e6)
        d = (e1 and e2 and e3 and e4) ^ (e1 and e2 and e3 and e5) ^ (
            e1 and e2 and e5 and e6) ^ (e2 and e3 and e4 and e6)
        e_ = (e4 and e2) ^ (e4 and e6)
        e = e_ and e1 and e3 and e5
        return a ^ b ^ c ^ d ^ e ^ 1  # according to changes specified by Dr Courtois

    def T(self, e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14,
          e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28):
        """ return [None, t1, t2, t3, t4, t5, t6, t7, t8, t9] """
        #print 'T', e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28
        from codegen import rvar

        def var(v, n):
            return rvar(v, n, self.current_instance, self.current_round)

        def var_T(v, n):
            return 'T_' + var(v, n)

        test_vectors = []

        ips_for_eq = [
            e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14,
            e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28
        ]
        for i in range(len(ips_for_eq)):
            test_vectors.append('{}={}'.format(var_T('E', i), ips_for_eq[i]))

        t1 = e0
        x1 = '{}={}'.format(var('T', 1), t1)

        t2 = t1 ^ self.Z(e1, e2, e3, e4, e5, e6, 1)
        x2 = '{}={}'.format(var('T', 2), t2)

        t3 = t2 ^ e7
        x3 = '{}={}'.format(var('T', 3), t3)

        t4 = t3 ^ self.Z(e8, e9, e10, e11, e12, e13, 2)
        x4 = '{}={}'.format(var('T', 4), t4)

        t5 = t4 ^ e14
        x5 = '{}={}'.format(var('T', 5), t5)

        t6 = t5 ^ self.Z(e15, e16, e17, e18, e19, e20, 3) ^ e1
        x6 = '{}={}'.format(var('T', 6), t6)

        t7 = t6 ^ e21
        x7 = '{}={}'.format(var('T', 7), t7)

        t8 = t7 ^ self.Z(e22, e23, e24, e25, e26, e27, 4)
        x8 = '{}={}'.format(var('T', 8), t8)

        t9 = t8 ^ e28
        x9 = '{}={}'.format(var('T', 9), t9)

        test_vectors += [x1, x2, x3, x4, x5, x6, x7, x8, x9]

        # The None isn't used
        self.test_vectors += test_vectors
        return [None, t1, t2, t3, t4, t5, t6, t7, t8, t9]

    def phi(self, s1, s2, f, U):
        from codegen import rvar, ret_str

        def var(v, n):
            return rvar(v, n, self.current_instance, self.current_round)

        def key_S(i, j=None):
            if j is None:
                j = self.current_round
                return ret_str('S', i, '%03d' % (j % 120))
            else:
                return ret_str('S', i, '%03d' % (j))
            return

        test_vectors = []
        """ phi is the round function. """

        # Notes
        # s1 and s2 are locals
        # U contains one round
        # nU is the next round

        nU = [None] + [0 for x in range(36)]
        t = self.T(f, s2,
                   *[U[self.long_term_key["P"][i]] for i in xrange(1, 28)])

        x1 = '{}={}'.format(key_S(2), s2)
        test_vectors.append(x1)

        for i in xrange(1, 28):
            x = '{}={}'.format(var('P', i), U[self.long_term_key["P"][i]])
            test_vectors.append(x)

        for j in range(1, 10):
            d = self.long_term_key["D"][j]

            if d is 0:
                # Because v[0] = s1
                # True for j == 1
                nU[4 * j - 3] = s1 ^ t[10 - j]
                x1 = '{}={}'.format(var('U', 4 * j - 3), nU[4 * j - 3])
                x2 = '{}={}'.format(key_S(1), s1)
                test_vectors += [x1, x2]
            else:
                nU[4 * j - 3] = U[d] ^ t[10 - j]
                x1 = '{}={}'.format(var('U', 4 * j - 3), nU[4 * j - 3])
                x2 = '{}={}'.format(var('D', j), U[d])
                test_vectors += [x1, x2]

            nU[4 * j - 2] = U[4 * j - 3]
            x1 = '{}={}'.format(var('U', 4 * j - 2), nU[4 * j - 2])

            nU[4 * j - 1] = U[4 * j - 2]
            x3 = '{}={}'.format(var('U', 4 * j - 1), nU[4 * j - 1])

            nU[4 * j] = U[4 * j - 1]
            x5 = '{}={}'.format(var('U', 4 * j), nU[4 * j])
            test_vectors += [x1, x3, x5]

        self.test_vectors += test_vectors
        return nU

    def PHI(self, s1, s2, f, U):

        def pretty_print(nU):
            nU = int(''.join(map(lambda x: str(x), nU)[1:]), 2)
            return hex(nU)

        U = format(U, '0>36b')
        U = [None] + [int(x) for x in U]
        #print U
        nU = self.phi(s1, s2, f, U)
        return nU

    def a(self, i):
        """ a[i] = u(i*127, alpha) """

        return self.u(i * 127)[self.long_term_key["alpha"]]

    def u(self, i):
        """ u(i) is the output of i th iteration of the round function """

        def __u_gen(i):
            self.current_round = i

            nextr = self.phi(self.s1[i % 120], self.s2[i % 120],
                             self.get_f(i), self.Ustate[i - 1])
            self.Ustate.append(nextr)
            self.u_iCounter = i

        while self.u_iCounter < i:
            __u_gen(self.u_iCounter + 1)
        #for m in self.Ustate:
        #    print m
        return self.Ustate[i]
