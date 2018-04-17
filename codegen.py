# Author : Om "Ethcelon" Bhallamudi
# Version : 1.b1
import random
import sys
import argparse

import os.path
from sys import platform

from config import KeyDict
from helpers import pp_eqn, pp_args, pretty_print, comment, ret_str
from helpers import genruns, write_runs_to_file
from helpers import parse_args, ArgParseError
from helpers import timed_process, write_csv
from helpers import get_command, get_filename
from helpers import bin2hex_str, bin2hex_str16, bin2hex_str60, bin2hex_str9

from argon import ARGON

D = None
P = None

comm = None

# TODO
# Om says: Maintaining state in module globals till I convert this to a class.

current_round = 0
current_instance = 1
iv_seed = 0
keynum = 26

def set_global_command(com2):
    global comm
    comm = ['./{}.exe'.format(com2), '.\\{}.exe'.format(com2)]


####################################################

def var(v, n):
    return ret_str(v, '%02d' % n, '%03d' % current_instance, '%04d' % current_round)

def rvar(v, n, i, r):
    return ret_str(v, '%02d' % n, '%03d' % i, '%04d' % r)

# Om says: A bad name for variables of the previous round...
def pre(v, n):
    return ret_str(v, '%02d' % n, '%03d' % current_instance, '%04d' % (current_round-1))

####################################################

def set_key_globals(key):
    global D, P, keynum

    P = KeyDict[key][0]
    D = KeyDict[key][1]
    keynum = key
    return

def key_S(i, j=None):
    if j is None:
        j = current_round
        return ret_str('S', i, '%03d' % (j % 120))
    else:
        return ret_str('S', i, '%03d' % (j))
    return

def get_key_as_eqs():
    equations = []

    def S_init(i, j):
        return ret_str('S', i, '%03d' % (j))
    # S1 : DO I FIX BITS HERE?
    # 111 don't actually need to do the corr bits as they are already rep with partity bit equations.
    for i in range(1, 121):
        if i not in []:
            x1 = key_S(1, i) + '=' + ret_str('k', '%03d' % i)
            equations.append(x1)
    for i in range(1, 121):
        if i not in []:
            x2 = key_S(2, i) + '=' + ret_str('k', '%03d' % (i+120))
            equations.append(x2)

    # PARTITY EQUATIONS

    for i in xrange(1, 6):
        x3= ''
        for m in xrange(1, 24):
            x3 += ret_str('k', '%03d' % (24*(i-1)+m ) ) + '+'
        x3 = ret_str('k', '%03d' % (24*i) ) + '=' + x3
        equations.append(x3 + '1')

        x4 = ''
        for m in xrange(1, 24):
            x4 += ret_str('k', '%03d' % (24*(i-1)+m+120 ) ) + '+'
        x4 = ret_str('k', '%03d' % ((24*i)+120) ) + '=' + x4
        equations.append(x4 + '1')

    #print len(equations)
    return equations

def get_k_fix_eqns(to_fix):
    equations = []
    for fix in to_fix:
        x = ret_str('k', '%03d' % (fix)) + '=1'
        equations.append(x)
    return equations

def set_partity(key):

    par_range = range(1, 24)
    for pp in range(1,11):
        par = 1
        for i in par_range:
            par = par ^ key[i-1]
        key[24*pp-1] = par

    return key

####################################################

def get_deterministic_iv():
    global iv_seed
    if iv_seed > 999:
        iv_seed = 0
    random.seed(iv_seed)
    F = random.getrandbits(61)
    iv_seed += 1
    F_str = format(F, '0>61b')

    return [int(f) for f in F_str]

def var_F(n):
    j=n
    return ret_str('F', '%04d' % (j), '%03d' % current_instance)

def get_f_eqn():
    n = current_round + 60 # We don't have
    return var_F(n) + '=' + '+'.join([var_F(n-61), var_F(n-60), var_F(n-59), var_F(n-56)])

def get_iv_eqns(IV):
    return [ret_str('F', '%04d' % (i), '%03d' % current_instance) + '=' + str(IV[i]) for i in range(len(IV))]

####################################################

def get_input_as_str(input_in_hex_as_string):
    # Not a general purpose conversion, only fits this purpose
    in_as_int = int(input_in_hex_as_string, 16)
    in_as_bin_str = format(in_as_int, '0>36b')
    return in_as_bin_str

def get_input_as_eq(ip): # ugly input
    equations = []
    for i in range(1, len(ip)+1):
        x = var('U', i) + '=' + str(ip[i-1])
        equations.append(x)
    return equations

def get_n_rounds_output_eqns(key, F, n):
    equations = []
    long_term_key = {
        "alpha" : 23,
        "D" : D,
        "P" : P,
    }
    engine = ARGON(long_term_key, F, key[:120], key[120:])

    x = engine.u(n)
    x = x[1:]
    x = [str(i) for i in x]
    op =''.join(x)
    x4 = get_input_as_eq(op)
    equations += x4

    return equations, op

####################################################

def get_z_eqns(z_n, inp):
    # Om says: Looks good! No need for changes
    # Om says: I'd rather call this Z, but it might be confused with the Z function in argon.py
    def var_Z(v, n):
        return 'Z_{}_'.format(z_n) + var(v, n)

    equations = []
    for i in range(1,7):
        x1 = var_Z('E', i) + '=' + inp[i-1]
        equations.append(x1)
    # Om says : Although equations are repr using x everywhere, I left these named
    #           like this to keep sanity while comparing to argon.
    e1 = var_Z('E', 1)
    e2 = var_Z('E', 2)
    e3 = var_Z('E', 3)
    e4 = var_Z('E', 4)
    e5 = var_Z('E', 5)
    e6 = var_Z('E', 6)

    # WARNING keep order
    local_vars  = [e1, e2, e3, e4, e5, e6]

    a = ['e1', 'e5', 'e6']
    b = ['e1*e4', 'e2*e3', 'e2*e5', 'e4*e5', 'e5*e6']
    c = ['e1*e3*e4', 'e1*e3*e6', 'e1*e4*e5', 'e2*e3*e6', 'e2*e4*e6', 'e3*e5*e6' ]
    d = ['e1*e2*e3*e4', 'e1*e2*e3*e5', 'e1*e2*e5*e6', 'e2*e3*e4*e6']
    e = ['e4*e2', 'e4*e6']
    f = ['e1*e3*e5']

    eqe = '+'.join(e)
    for i in range(1, 7): eqe = eqe.replace('e%d' % i, local_vars[i-1])
    xy = var_Z('W', 1) + '=' + eqe
    equations+= [xy]

    eqea = '+'.join(f)
    for i in range(1, 7): eqea = eqea.replace('e%d' % i, local_vars[i-1])
    xz = var_Z('H', 5) + '=' + var_Z('W', 1)+'*'+ eqea
    equations+= [xz]

    # WARNING keep order
    eqs = [a, b, c, d]
    eqs2 = []
    for eq in eqs:
        eq = '+'.join(eq)
        for j in range(1, 7):
            eq = eq.replace('e%d' % j, local_vars[j-1])
        eqs2.append(eq)

    for i in range(1,5):
        x2 = var_Z('H', i) + '=' + eqs2[i-1]
        equations += [x2]

    x33 = '+'.join([var_Z('H', 1), var_Z('H', 2), var_Z('H', 3), var_Z('H', 4), var_Z('H', 5), '1'])
    x3 = var('Z_O', z_n) + '=' + x33
    equations += [x3]

    return equations

def get_t_eqns():

    def var_T(v, n):
        return 'T_' + var(v, n)

    def var_Z(v, n):
        return 'Z_{}_'.format(z_n) + var(v, n)

    equations = []

    x1 = var_T('E', 0) + '=' + var_F(current_round+60)
    x2 = get_f_eqn()


    x3 = var_T('E', 1) + '=' + key_S(2) # ugly
    equations += [x1, x2 ,x3]

    for i in range(2, 29):
        p = P[i-1]
        x4 = var_T('E', i) + '=' + var('P', i-1)
        x5 = var('P', i-1) + '=' + pre('U', p)
        equations += [x4, x5]

    t1 = var('T', 1) + '=' + var_T('E', 0)
    t2 = var('T', 2) + '=' + var('T', 1) + '+' + var('Z_O', 1 )
    t3 = var('T', 3) + '=' + var('T', 2) + '+' + var_T('E', 7)
    t4 = var('T', 4) + '=' + var('T', 3) + '+' + var('Z_O', 2 )
    t5 = var('T', 5) + '=' + var('T', 4) + '+' + var_T('E', 14)
    t6 = var('T', 6) + '=' + var('T', 5) + '+' + var('Z_O', 3 ) + '+' + var_T('E', 1)
    t7 = var('T', 7) + '=' + var('T', 6) + '+' + var_T('E', 21)
    t8 = var('T', 8) + '=' + var('T', 7) + '+' + var('Z_O', 4 )
    t9 = var('T', 9) + '=' + var('T', 8) + '+' + var_T('E', 28)
    z1 = get_z_eqns(1, [var_T('E', i) for i in [1, 2, 3, 4, 5 ,6] ])
    z2 = get_z_eqns(2, [var_T('E', i) for i in [8, 9, 10, 11, 12 ,13] ])
    z3 = get_z_eqns(3, [var_T('E', i) for i in [15, 16, 17, 18, 19 ,20] ])
    z4 = get_z_eqns(4, [var_T('E', i) for i in [22, 23, 24, 25, 26 ,27] ])
    equations += z1
    equations += z2
    equations += z3
    equations += z4
    equations += [t1, t2, t3, t4, t5, t6, t7, t8, t9]

    return equations

def get_round_eqns(r):
    global current_round
    current_round = r
    # A long tme ago rounds were managed within this function,
    # A very bad idea!
    equations = []

    #comment(round=current_round)
    t_eqns = get_t_eqns()
    equations += t_eqns

    for j in range(1, 10):
        d = D[j]

        if d is 0:
            # Don't be confused by the next line, str % something is formatting, int % something is modulus!
            x1 = var('U', 4*j-3) + '=' + key_S(1) + '+' + var('T', 10-j)
            equations += [x1]
        else:
            x1 = var('U', 4*j-3) + '=' + var('D', j) + '+' + var('T', 10-j)
            x2 = var('D', j) + '=' + pre('U', d)
            equations += [x1, x2]

        x3 = var('U', 4*j-2) + '=' + pre('U', 4*j-3)
        x4 = var('U', 4*j-1) + '=' + pre('U', 4*j-2)
        x5 = var('U', 4*j-0) + '=' + pre('U', 4*j-1)
        equations += [x3, x4, x5]

    #comment(number_of_eqs=len(equations))

    return equations

def do_runs(runs, actions, passalong):
    global current_instance, current_round
    import sys

    runs_output=[]
    vectors = []

    run_id = 0
    realtime = open('realtime.txt', 'w')

    comment('I check realtime.txt for live updates!')
    pretty_print('I check realtime.txt for live updates!')

    for run in runs:
        equations = []
        test_vectors = []
        to_fix = []
        round_vectors = []

        run_id += 1
        comment('='*16, '='*16, 'run %s' % str(run))

        fix = run['fix']
        rounds = run['rounds']
        ins = run['ins']

        cmd = get_command(sys.argv[0], run, actions)
        filename = get_filename(run, actions)

        x1 = get_key_as_eqs()
        equations += x1
        comment(num_of_key_eqns=len(x1))

        if fix is 0:
            comment("No bits fixed")
        else:
            random.seed()
            all_bits = range(1, 241)
            # WE DONT REALLY WANT ALL BITS!
            all_bits = []
            for bb in range(1, rounds+1):
                all_bits += [bb, bb+120]

            comment("sampling fixes from:" + str(all_bits))
            pretty_print("I sampling fixes from:" + str(all_bits))

            partiy_bits = [24, 48, 72, 96, 120, 24+120, 48+120, 72+120, 96+120, 120+120]
            for p in partiy_bits:
                if p in all_bits:
                    all_bits.remove(p)

            if int(fix) > len(all_bits):
                fix = len(all_bits)


            to_fix = random.sample(all_bits, int(fix))
            to_fix = sorted(to_fix)
            kfixes_eq = get_k_fix_eqns(to_fix)
            comment('{} bits fixed'.format(len(to_fix)))

            test_vectors += kfixes_eq
            equations += kfixes_eq

        key_to_gen_default = 'ABCD1ABCD2ABCD3ABCD4ABCD5ABCD6ABCD7ABCD8ABCD9ABCDAABCDBABCDC'

        key_to_gen_default_bits = format(int(key_to_gen_default, 16), 'b')

        key_generated = [int(bii) for bii in key_to_gen_default_bits]

        for bit in to_fix:
            key_generated[bit-1] = 1

        key_generated = set_partity(key_generated)

        x88 = []
        for mn in range(len(key_generated)):
            x88.append( '{}={}'.format(ret_str('k', '%03d' % (mn+1)), key_generated[mn]) )

        test_vectors += x88

        for instance in xrange(1, ins+1):
            current_instance = instance
            current_round = 0

            comment('Instance {}'.format(instance))

            F = get_deterministic_iv() # len 61
            iv = ''.join([str(i) for i in F])
            x3 = get_iv_eqns(F)
            equations += x3

            comment(iv_eqns=len(x3))

            x4 = get_input_as_str('69C7C85A3')
            x4 = get_input_as_eq(x4)
            equations += x4

            if rounds > 0:
                for r in range(1, rounds+1):
                    x5 = get_round_eqns(r)
                    equations += x5
                comment(no_rounds_to_gen=r)
            else:
                pass

            x45 = []

            long_term_key_for_engine = {
                "alpha" : 23,
                "D" : D,
                "P" : P,
            }

            engine = ARGON(long_term_key_for_engine, F, key_generated[:120], key_generated[120:])
            engine.set_current_instance(current_instance)

            x456 = engine.u(rounds)
            x456 = x456[1:]
            x456 = [str(i) for i in x456]
            op =''.join(x456)

            x4 = get_input_as_eq(op)
            x45 += x4

            equations += x45
            comment(output_equations=len(x45))

            kkkey = ''.join([str(i) for i in key_generated])

            test_vectors += engine.get_test_vectors()

            curr_vector = ('69C7C85A3', bin2hex_str9(op), bin2hex_str60(kkkey),rounds ,bin2hex_str16(iv), keynum)
            round_vectors.append(curr_vector)

        comment('='*16, instances=instance, total_no_equations=len(equations))

        with open(filename + '.txt', 'w') as f:

            def fcomment(*args, **kwargs):
                "Prints args & kwgars to stdout, uses a delimiter ( typically // )."
                delimiter = '//'
                for arg in args:
                    f.write('{delimiter} {com}\n'.format(com=arg, delimiter=delimiter))
                for key, value in kwargs.iteritems():
                    f.write('{delimiter} {key} = {value}\n'.format(key=key, value=value, delimiter=delimiter))

            def wreq(equations):
                for eq in equations:
                    f.write('{}\n'.format(eq))

            # Write comments
            fcomment(command=cmd, run=run, actions=actions, passalong=passalong)
            fcomment(num_of_key_eqns=len(x1), num_of_parity_eqns=10, num_of_iv_eqns=len(x3))
            fcomment(generated_instances=instance, generated_rounds=rounds)
            fcomment(total_number_of_equations=len(equations))
            fcomment('vectors (in hex, also written to vectors.csv)')
            vectors += round_vectors
            for vector in round_vectors:
                fcomment('+++',ip=vector[0], op=vector[1], key=vector[2], rounds=vector[3], iv=vector[4], lzs=vector[5])

            if len(vectors) == 0: fcomment('+++')

            # Write equations
            wreq(equations)
            comment('W {} equations written to {}.txt'.format(len(equations), filename))
            pretty_print('W {} equations written to {}.txt'.format(len(equations), filename))
            f.close()

        with open(filename+'_solution.txt', 'w') as f:
            def fcomment(*args, **kwargs):
                "Prints args & kwgars to stdout, uses a delimiter ( typically // )."
                delimiter = '//'
                for arg in args:
                    f.write('{delimiter} {com}\n'.format(com=arg, delimiter=delimiter))
                for key, value in kwargs.iteritems():
                    f.write('{delimiter} {key} = {value}\n'.format(key=key, value=value, delimiter=delimiter))

            def wreq(eqs):
                for eq in eqs:
                    f.write('{}\n'.format(eq))

            fcomment(generated_instances=instance, generated_rounds=rounds)
            fcomment(command=cmd, run=run, actions=actions, passalong=passalong)

            for vector in round_vectors:
                fcomment('+++',ip=vector[0], op=vector[1], key=vector[2], rounds=vector[3], iv=vector[4], lzs=vector[5])

            wreq(test_vectors)

            comment('W {} solutions written to {}_solution.txt'.format(len(test_vectors), filename))
            pretty_print('W {} solutions written to {}_solution.txt'.format(len(test_vectors), filename))

            f.close()

        #if 'printequationsprettilyplease' in passalong:
        #    pp_eqn(equations)

        mode_ = None

        if platform == "linux" or platform == "linux2":
            comm_ = comm[0]
        elif platform == "darwin":
            comm_ = comm[0]
        elif platform == "win32":
            comm_ = comm[1]

        if actions['sat'] and actions['xl']:
            mode_ = '4444 /deg4'
        elif actions['xl']:
            mode_ = '4000 /deg4'

        if mode_ is not None and comm is not None:
            proc = ' '.join([comm_, mode_, filename+'.txt'])#+passalong)
            try:
                comment('C {}'.format(proc))
                pretty_print('C {}'.format(proc))

                time_it_took = timed_process(proc)
                comment('C ax64 returned')

                run_str = 'rounds={},ins={},fix={}'.format(rounds, ins, fix)
                run_str_2 = '{}, {}\n'.format(run_id, time_it_took)

                runs_output.append((run_id, run_str ,time_it_took))
                realtime.write(run_str_2)
            except Exception as e:
                raise e

    realtime.close()
    return runs_output, vectors

def main(parsed_args):
    
    pp_args(parsed_args)

    if 'key' in parsed_args.keys():
        set_key_globals(int(parsed_args['key']))
    else:
        set_key_globals(26)

    if 'old' in parsed_args.keys():
        set_global_command(parsed_args['old'])
    else:
        set_global_command('ax64')

    runs, actions, passalong = genruns(parsed_args)
    comment(total_runs=len(runs), actions=actions, passalong=passalong)

    fname = 'runs.txt'
    comment('W {} runs to {}'.format(len(runs), fname))
    pretty_print('W {} runs to {}'.format(len(runs), fname))

    write_runs_to_file(runs, actions, passalong, fname)
    comment('='*16, 'running...')
    runs_output, vectors = do_runs(runs, actions, passalong)
    comment('='*16, 'done!')
    write_csv('times.csv','NO.,TIME' ,runs_output)
    write_csv('vectors.csv','IP,OP,KEY,ROUNDS,IV,LZS' ,vectors)

    comment('W {} runtimes to times.csv'.format(len(runs_output)))
    pretty_print('W {} runtimes to times.csv'.format(len(runs_output)))

    comment('W {} test vectors written vectors.csv'.format(len(vectors)))
    pretty_print('W {} test vectors written vectors.csv'.format(len(vectors)))


if __name__ == '__main__':
    # try catch around this please!
    parsed_args = parse_args(sys.argv)
    main(parsed_args)
